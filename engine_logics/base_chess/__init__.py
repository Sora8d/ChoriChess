from debug import func_info
import random
from PIL import Image
from pathlib import Path
from engine_logics.base_chess.board_and_pieces import board, pieces

#TODO
#Create check and checkmate
#Create turns

def cli_promotion():
    print('What do you want this Pawn to be?')
    selection= input('Q/B/N/R \n')
    return selection

class Game_Chess():
    turn_dict={'w': 1, 'b': 0}
    def __init__(self, promotion_func=cli_promotion, use_imgs=True):
        self.turn= 1
        self.n_turn= 0
        self.board= board.Board(promotion_func)
        self.players= []
        self.game= 0
        self.winner= None
        self.use_imgs= use_imgs
#Stuff about importing games
        self.imported= False
        self.player_and_turn_desired = None

    def add_player(self, player):
        if len(self.players) < 2:
            self.players.append(player)
        if len(self.players) == 2  and self.game == 0:
            self.players= random.sample(self.players, 2)

    def startgame(self):
        self.game= 1
        self.correct_playerturn() if self.imported else self.board.set_up_start_pieces()
        self.move_handler(5,'Game Set Up')

    def endgame_check(self):
        en_k_check= self.board.king_move_check(self.n_turn, self.turn)
        if [] == [j for i in en_k_check.values() for j in i]:
            k_check= self.board.king_move_check(self.turn, self.n_turn)
            self.game= 0
            if self.board.pieces[self.n_turn]['K'][0].position in [j for i in k_check.values() for j in i]:
                self.winner= self.turn
                return self.move_handler(3, 'Checkmate, winner is '+str(self.players[self.winner]))
            else:
                self.winner= 2
                return self.move_handler(3, 'Draw')
        else:
            return None


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
        if self.players[self.turn] != player:
            return self.move_handler(4, "Its not your turn")
#Pure the moves

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
        self.player_and_turn_desired = player_and_turn_desired
        return

    def FEN_pieces_implementation(self, notation):
        rows= notation.split('/')[::-1]
        for x in range(len(rows)):
            spaces_blank_behind= 0
            for i in range(len(rows[x])):
                piece= rows[x][i]
                if piece.isnumeric():
                    spaces_blank_behind += int(piece)-1
                    continue
                correction= (i)+(spaces_blank_behind)
                position= '{}{}'.format(chr(97+correction), x+1)
                importing_pieces_dict[piece.upper()](position, piece.isupper(), self.board)

    def FEN_castling_implementation(self, _notation):
        #This is because the 0 indexed if the list is not reversed is the white instruction
        #but 0 is black in the pieces.
        _qk_dict= {'K': 1, 'Q': 0}
        _qk_reference= 'KQkq'
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

        #else:
        #    _missing_castles= []
        #    for x in _qk_reference:
        #        if x not in _notation:
        #            _missing_castles.append(x)
        #    for x in _missing_castles:
        #        self.board.pieces[x.isupper()]['R'][_qk_dict[x.upper()]].last_movement = 'e1'

    @func_info
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
        if self.players[turn_desired] != player:
            self.players= self.players[::-1]


importing_pieces_dict= {
    'P': pieces.Pawn,
    'B': pieces.Bishop,
    'Q': pieces.Queen,
    'K': pieces.King,
    'R': pieces.Rook,
    'N': pieces.Knight
}