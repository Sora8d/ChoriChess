from typing import final
from engine_logics.errors.chess_errors_handler import Error_handler_notation_general, Error_handler_pieces_implementation
import random
from PIL import Image
from pathlib import Path
from engine_logics.base_chess.board_and_pieces import board, pieces


def cli_promotion():
    print('What do you want this Pawn to be?')
    selection= input('Q/B/N/R \n')
    return selection

def transform_pos_to_FEN(func):
    _upper_lower= {1:lambda x: x.upper(), 0:lambda x: x.lower()}
    def wrapper(self, state, msg):
        result=func(self,state,msg)
        if state != 0 and state != 4:
            _board = self.board
            _pieces= _board.pieces
            final_notation= ""
            #arranging pieces
            _pieces_notation= ''
            _spaces_blank= 0
            #Since dicts are now ordered this just works

            for x in range(1,9):
                for i in range(8):
                    ichar=chr(97+i)
                    position= ichar+str(x)
                    print(position)
                    piece_in_position= _board.table[position]                  
                    if piece_in_position == None and ichar != 'h':
                        _spaces_blank+=1
                    else:
                        if _spaces_blank > 0: 
                            _pieces_notation+= str(_spaces_blank)
                            _spaces_blank=0
                        if piece_in_position!= None:
                            _pieces_notation += _upper_lower[piece_in_position.colour](piece_in_position.type)
                        if ichar == 'h':
                            _pieces_notation+= '/'
            final_notation= _pieces_notation+' '
            #writing turn
            final_notation += {1:'w',0:'b'}[self.turn]+' '
            #arranging castling
            _castle_no= '-'
            _castle_yes= ''
            for king in _pieces[1]['K']+_pieces[0]['K']:
                if king.last_movement == None:
                    for rook in _pieces[king.colour]['R']:
                        if rook.last_movement == None:
                            _castle_yes += _upper_lower[rook.colour]({'a':'Q', 'h':'K'}[rook.position[0]])
            final_notation+= _castle_no if _castle_yes == '' else _castle_yes
            final_notation+=' '
            #arranging en_peassant
            final_notation += '-' if _board.en_peassant == False else _board.lm_piece.position
            final_notation+=' '
            self.FEN_of_current_board= final_notation
            print(self.FEN_of_current_board)
        return result
    return wrapper

class Game_Chess():
    turn_dict={'w': 1, 'b': 0}
    def __init__(self, promotion_func=cli_promotion, use_imgs=True):
        self.turn= 1
        self.n_turn= 0
        self.board= board.Board(promotion_func)
        self.players= {'list': []}
        self.game= 0
        self.winner= None
        self.use_imgs= use_imgs
#Stuff about importing games
        self.imported= False
        self.player_and_turn_desired = None

        self.create_exceptions()

    def create_exceptions(self):
        self.error= ValueError

    def add_player(self, player):
        if len(self.players['list']) < 2:
            self.players['list'].append(player)
        if len(self.players['list']) == 2  and self.game == 0:
            self.players['list']= random.sample(self.players['list'], 2)

    def startgame(self):
        self.game= 1
        if not self.imported: self.board.set_up_start_pieces()
        elif self.player_and_turn_desired != None: 
            self.correct_playerturn()
        self.move_handler(5,'Game Set Up')

    def endgame_check(self):
        en_k_check= self.board.king_move_check(self.n_turn, self.turn)
        if [] == [j for i in en_k_check.values() for j in i]:
            k_check= self.board.king_move_check(self.turn, self.n_turn)
            self.game= 0
            if self.board.pieces[self.n_turn]['K'][0].position in [j for i in k_check.values() for j in i]:
                self.winner= self.turn
                return self.move_handler(3, 'Checkmate, winner is '+str(self.players['list'][self.winner]))
            else:
                self.winner= 2
                return self.move_handler(3, 'Draw')
        else:
            return None

    @transform_pos_to_FEN
    def move_handler(self, state, msg):
        if state != 0 and state != 4 and self.use_imgs:
            self.img_s()
        return state, msg

#If movement is valid creates the board img
    def img_s(self):
        invert_n= [7,6,5,4,3,2,1,0]
        self.board.c_img = self.board.b_img.copy()
        for x in self.board.pieces:
            for i in self.board.pieces[x]:
                for z in self.board.pieces[x][i]:
                    self.board.c_img.paste(z.img, (128*(ord(z.position[0])-97), 128*(invert_n[int(z.position[1])-1])), z.img)
        self.board.c_img.show()
        return

    def move(self, player, move):
        if self.game == 0:
            return self.move_handler(0, "Game Over")
        if self.players['list'][self.turn] != player:
            return self.move_handler(4, "Its not your turn")
        #Capture possible moves
        k_check= self.board.king_move_check(self.turn, self.n_turn)
        # This gives every value in k_check        [j for i in k_check.values() for j in i]
        #Castling
        if move == 'OO' or move == 'OOO':
            state= self.castle(move)
            w_t_r= {1: 'Castled '+move, 0: 'Invalid'+move}
            if state == 1:
                #Win cond.
                game_over=self.endgame_check()
                if game_over != None:
                    return game_over

                self.turn_change()
            return self.move_handler(state, w_t_r[state])
        if len(move) == 2:
            piece= 'P'
        else:
            piece = move[0]
            move = move[1:]
        if piece not in k_check:
            return self.move_handler(0, 'No valid piece')
        if move in k_check[piece]:
            quant= []
            for x in self.board.pieces[self.turn][piece]:
                if move in x.check_pos():
                    quant.append(x)
            if len(quant) == 1:
                quant[0].movement(move)
                #Win cond.
                game_over=self.endgame_check()
                if game_over != None:
                    return game_over
                self.turn_change()
                return self.move_handler(1, self.board.table[move].name + " moved to " + move)
            #Makes player to choose between the pieces
            else:
                quant_chosen = self.mul_pieces(quant)
                if quant_chosen == 0:
                    return self.move_handler(0, "No valid movement")
                quant_chosen.movement(move)
                #Win cond.
                game_over=self.endgame_check()
                if game_over != None:
                    return game_over
                self.turn_change()
                return self.move_handler(1, str(self.board.table[move].position) + " moved to " + move)
        return self.move_handler(0, "No valid movement")

    def castle(self, move):
        _numbah= {1: '1', 0: '8'}[self.turn]
        if self.board.pieces[self.turn]['K'][0].last_movement == None:
            _rooks_atc= []
            for x in self.board.pieces[self.turn]['R']:
                if x.last_movement == None:
                    _rooks_atc.append(x)
            if move == 'OO':
                for x in _rooks_atc:
                    if x.position == 'h'+_numbah:
                        self.board.pieces[self.turn]['K'][0].av_moves.append('g'+_numbah)
                        x.av_moves.append('f'+_numbah)
                        self.board.pieces[self.turn]['K'][0].movement('g'+_numbah)
                        x.movement('f'+_numbah)
                        return 1

            elif move == 'OOO':
                for x in _rooks_atc:
                    if x.position == 'a'+_numbah:
                        self.board.pieces[self.turn]['K'][0].av_moves.append('c'+_numbah)
                        x.av_moves.append('d'+_numbah)
                        self.board.pieces[self.turn]['K'][0].movement('c'+_numbah)
                        x.movement('d'+_numbah)
                        return 1
        return 0


    def turn_change(self):
        self.turn, self.n_turn = self.n_turn, self.turn

    def mul_pieces(self, quant):
        for x in range(len(quant)):
            print(str(x)+': '+ quant[x].type + 'in' +quant[x].position)
        election=int(input('Input the number of the piece u want to move \n'))
        if len(quant)-1 < election:
            return 0
        else:
            return quant[election]

#A function that serves the purpose of importing boards, now not every game needs to start from zero.
#For now it will just get the turn and positions, later castling information will be added

    def import_board(self, fen_notation, player_and_turn_desired):
        fen_notation= fen_notation.split(' ')
        Error_handler_notation_general(fen_notation, self.error)
        board= fen_notation[0]
        self.FEN_pieces_implementation(board)
        
        castles= fen_notation[2]
        self.FEN_castling_implementation(castles)

        en_peassant= fen_notation[3]
        self.FEN_en_peassant_implementation(en_peassant)

        _imported_turn= self.__class__.turn_dict[fen_notation[1]]
        if _imported_turn != self.turn:
            self.turn_change()
        self.imported = True
        if len(player_and_turn_desired) == 2:
            self.player_and_turn_desired = player_and_turn_desired
        return

    def FEN_pieces_implementation(self, notation):
        rows= notation.split('/')[::-1]
        Error_handler_pieces_implementation(rows, self.error)
        for x_number,x_string in enumerate(rows):
            spaces_blank_behind= 0
            for i_number, i_piece_or_blank_space in enumerate(x_string):
                piece= i_piece_or_blank_space
                if piece.isnumeric():
                    spaces_blank_behind += int(piece)-1
                    continue
                correction= (i_number)+(spaces_blank_behind)
                position= '{}{}'.format(chr(97+correction), x_number+1)
                importing_pieces_dict[piece.upper()](position, piece.isupper(), self.board)

    def FEN_castling_implementation(self, _notation):
        #This is because the 0 indexed if the list is not reversed is the white instruction
        #but 0 is black in the pieces.
        _ref_to_rook= {'K': 'h1', 'k': 'h8', 'Q': 'a1', 'q': 'a8'}
        if _notation == '-':
            self.board.pieces[1]['K'][0].last_movement= 'e1'
            self.board.pieces[0]['K'][0].last_movement= 'e1'
        else:
            _castle_allowed= []
            for x in self.board.pieces[1]['R']+self.board.pieces[0]['R']:
                for i in _notation:
                    if x.position == _ref_to_rook[i]:
                        x.last_movement= None
                        _castle_allowed.append(x)
                    elif x not in _castle_allowed:
                        x.last_movement= 'e1'


    def FEN_en_peassant_implementation(self, _notation):
        if _notation == '-':
           return
        self.board.en_peassant = _notation
        _en_peassant_dict= {'3': ['2', '4'], '6': ['7', '5']}
        _en_p_selection= _en_peassant_dict[_notation[1]]
        _piece= self.board.table[_notation[0]+_en_p_selection[1]]
        _last_movement= _notation[0]+_en_p_selection[0]
        self.board.lm_piece= _piece
        _piece.last_movement= _last_movement
        pass
        
#Corrects when importing a game that white and black players are correct.
    def correct_playerturn(self):
        player= self.player_and_turn_desired[0]
        turn_desired= self.__class__.turn_dict[self.player_and_turn_desired[1]]
        if self.players['list'][turn_desired] != player:
            self.players['list']= self.players['list'][::-1]


importing_pieces_dict= {
    'P': pieces.Pawn,
    'B': pieces.Bishop,
    'Q': pieces.Queen,
    'K': pieces.King,
    'R': pieces.Rook,
    'N': pieces.Knight
}