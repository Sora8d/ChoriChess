import copy, random
from PIL import Image
import PIL
from pathlib import Path
#TODO
#Create check and checkmate
#Create turns

def cli_promotion():
    print('What do you want this Pawn to be?')
    selection= input('Q/B/N/R \n')
    return selection

promotion_choose= {}

class Board():
    def __init__(self, promotion_choosing):
        self.create_table()
        self.create_pieces_dict()
#Last moved piece
        self.lm_piece= ""
#Available moves
        self.av_moves= []
#Image of board
        self.b_img= Image.open('images/tablero_{}.png'.format(random.randint(1,4)))
        self.c_img=self.b_img.copy()
#Method of promotion of pawns
        self.promotion_choosing= promotion_choosing

#Creates board dict
    def create_table(self):
        self.table = {}
        for x in range(1,9):
            Letter= chr(x+96)
            for i in range(1,9):
                self.table[Letter + str(i)] = None
#Creates pieces dict

    def create_pieces_dict(self):
        self.pieces = {}
        self.pieces[1] = {}
        self.pieces[0] = {}
        for x in range(0, 2):
            self.pieces[x]['P']= []
            self.pieces[x]['R']= []
            self.pieces[x]['K']= []
            self.pieces[x]['B']= []
            self.pieces[x]['Q'] = []
            self.pieces[x]['N'] = []

    def set_up_start_pieces(self):
#Setting Pawns. This and the other types of pieces are not appended anywhere cuz the Piece's classes append themselves, so this is a lil confusing.
        for x in range(1,9):
            Letter= chr(x+96)
            pawnw=Pawn(Letter + str(2), 1, self)
            # self.pieces[1]['P'].append(pawnw)

            pawnb=Pawn(Letter + str(7), 0, self)
            # self.pieces[0]['P'].append(pawnb)

#Setting other pieces
        Pieces={
        1:{
        'R': [Rook('a1', 1, self), Rook('h1', 1, self)],
        'B': [Bishop('c1', 1, self), Bishop('f1', 1, self)],
        'N': [Knight('b1', 1, self), Knight('g1', 1, self)],
        'Q': [Queen('d1', 1,self)],
        'K': [King('e1', 1, self)]
        },
        0:{
        'R': [Rook('a8', 0, self), Rook('h8', 0, self)],
        'B': [Bishop('c8', 0, self), Bishop('f8', 0, self)],
        'N': [Knight('b8', 0, self), Knight('g8', 0, self)],
        'Q': [Queen('d8', 0,self)],
        'K': [King('e8', 0, self)]
        }
        }
        # for x, i in Pieces.items():
            # for y, z in i.items(): self.pieces[x][y].extend(z)
#Checking moves, for the pawns it has to extract the move from the en_peassant marker, it gives it to a dictionary that has the Piece object as key and the moves as pair
    def check_moves(self, turn):
        all_moves= {'P': [], 'K': [], 'N': [], 'Q': [], 'R': [], 'B': []}
        for x in self.pieces[turn]:
            for i in self.pieces[turn][x]:
                p= i.check_pos()
                all_moves[x].extend(p)
#This returns a dict as {'P': [...], 'B': [...] etc}
        return all_moves

#Creates a copy of the board, to check if any of the moves puts its own king in check
#At first, this was supposed to return m_t_check without the check dangers, but for some reasons there are cases where
#some movements are overlooked (try to get a checkmate, it wont happen). For further info check "BUG.txt"
#So now instead of returning m_t_check, all the accepted movements are moved to a new dict, and that is returned
#Now overlooked movements will not appear, but further testing will have to check if movements supposed to be avaiable are
#also skipped, until now al ocurrences were under checkmate.
    def king_move_check(self, turn, e_turn):
        m_t_check=self.check_moves(turn)
        acc_moves= {}
        promotion_choose[str(self.__class__)] = self.promotion_choosing
        self.promotion_choosing = lambda: 1
        for x, i in m_t_check.items():
            if i == []:
                continue
            else:
                for l in i:
                    b_c= copy.deepcopy(self)
                    for t in b_c.pieces[turn][x]:
                        V= t.movement(l)
                        if V == 0:
                            continue
                        ene_check= []

                        [ene_check.extend(i) for (x,i) in b_c.check_moves(e_turn).items()]
                        if self.pieces[turn]['K'][0].position in ene_check or x == "K" and t.position in ene_check:
                            continue
                        else:
                            acc_moves.setdefault(x, [])
                            acc_moves[x].append(l)
        self.promotion_choosing = promotion_choose[str(self.__class__)]
        print(self.promotion_choosing)
        return acc_moves


#The mother-class piece
class Piece():
    name=''
    type=''
    default_img= {0:Image.open(Path('images/peon_b.png')), 1:Image.open(Path('images/peon.png'))}
    def __init__(self, position, colour, board, img=None):
        self.position= position
        self.colour= colour
        self.board= board
        self.last_movement= None
        self.av_moves= []
# IMG STUFF
        self.img= self.__class__.default_img[colour] if img == None else img
        self.img= self.img.convert('RGBA')
# ------------
        self.board.table[position] = self
        self.board.pieces[self.colour][self.type].append(self)

# ------------
    def prrint(self):
        print(self.position)

    def movement(self, position, en_p=0):
        self.board.table[self.position] = None
        n_p= self.board.table[position]
        if n_p != None:
            self.board.pieces[n_p.colour][n_p.type].remove(n_p)
        if en_p != 0:
            en_p = self.board.table[en_p]
            self.board.pieces[en_p.colour][en_p.type].remove(en_p)
        self.board.table[position] = self
        self.last_movement= self.position
        self.position = position
        self.board.lm_piece= self
        return

class Rook(Piece):
    name='Rook'
    type='R'
    default_img= {0:Image.open(Path('images/torre_b.png')), 1:Image.open(Path('images/torre.png'))}
    def check_pos(self):
        c_checking= self.position
        v_moves= []
        x= 1
        while c_checking[0] != 'h':
            c_checking= chr(ord(c_checking[0])+x)+c_checking[1]
            if self.board.table[c_checking] == None:
                v_moves.append(c_checking)
            elif self.board.table[c_checking].colour != self.colour:
                v_moves.append(c_checking)
                break
            else:
                break
        c_checking= self.position
        x= 1
        while c_checking[0] != 'a':
            c_checking= chr(ord(c_checking[0])-x)+c_checking[1]
            if self.board.table[c_checking] == None:
                v_moves.append(c_checking)
            elif self.board.table[c_checking].colour != self.colour:
                v_moves.append(c_checking)
                break
            else:
                break
        c_checking= self.position
        x= 1
        while c_checking[1] != '8':
            c_checking= c_checking[0]+str(int(c_checking[1])+x)
            if self.board.table[c_checking] == None:
                v_moves.append(c_checking)
            elif self.board.table[c_checking].colour != self.colour:
                v_moves.append(c_checking)
                break
            else:
                break
        c_checking= self.position
        x= 1
        while c_checking[1] != '1':
            c_checking= c_checking[0]+str(int(c_checking[1])-x)
            if self.board.table[c_checking] == None:
                v_moves.append(c_checking)
            elif self.board.table[c_checking].colour != self.colour:
                v_moves.append(c_checking)
                break
            else:
                break
        self.av_moves= v_moves

        return self.av_moves
    def movement(self, position):
        valid= ""
        if position in self.av_moves:
            valid= True
        if valid:
            super().movement(position)
            return 1
        return 0

class Bishop(Piece):
    name='Bishop'
    type='B'
    default_img= {0:Image.open(Path('images/alfil_b.png')), 1:Image.open(Path('images/alfil.png'))}
#New Method, check all available movements
    def check_pos(self):
        c_checking= self.position
        v_moves= []
        x= 1
        while c_checking[0] != 'h' and c_checking[1] != '8':
#This transforms the letter into an integer, sums/rests by x, and combines with the number also summed or rested by x
            c_checking= chr(ord(c_checking[0])+x)+str(int(c_checking[1])+x)
            if self.board.table[c_checking] == None:
                v_moves.append(c_checking)
            elif self.board.table[c_checking].colour != self.colour:
                v_moves.append(c_checking)
                break
            else:
                break
        c_checking= self.position
        x= 1
        while c_checking[0] != 'h' and c_checking[1] != '1':
            c_checking= chr(ord(c_checking[0])+x)+str(int(c_checking[1])-x)
            if self.board.table[c_checking] == None:
                v_moves.append(c_checking)
            elif self.board.table[c_checking].colour != self.colour:
                v_moves.append(c_checking)
                break
            else:
                break
        c_checking= self.position
        x= 1
        while c_checking[0] != 'a' and c_checking[1] != '8':
            c_checking= chr(ord(c_checking[0])-x)+str(int(c_checking[1])+x)
            if self.board.table[c_checking] == None:
                v_moves.append(c_checking)
            elif self.board.table[c_checking].colour != self.colour:
                v_moves.append(c_checking)
                break
            else:
                break
        c_checking= self.position
        x= 1
        while c_checking[0] != 'a' and c_checking[1] != '1':
            c_checking= chr(ord(c_checking[0])-x)+str(int(c_checking[1])-x)
            if self.board.table[c_checking] == None:
                v_moves.append(c_checking)
            elif self.board.table[c_checking].colour != self.colour:
                v_moves.append(c_checking)
                break
            else:
                break
        self.av_moves= v_moves
        return self.av_moves

    def movement(self, position):
        valid= ""
#This one checks that the movement is in diagonal, it rests the original position to the movement, and elevates to the power of 2 (to ignore +-) and compares
        if position in self.av_moves:
            valid= True
        if valid:
            super().movement(position)
            return 1
        return 0

class Knight(Piece):
    name= 'Knight'
    type= 'N'
    default_img= {0:Image.open(Path('images/horse_b.png')), 1:Image.open(Path('images/horse.png'))}
    def check_pos(self):
        c_checking= self.position
        v_moves= []
        x= ([2, -2], [1,-1])
        for i in x[0]:
            for y in x[1]:
                c_move= chr(ord(c_checking[0])+i)+str(int(c_checking[1])+y)
                try:
                    if self.board.table[c_move] == None or self.board.table[c_move].colour != self.colour:
                        v_moves.append(c_move)
                except KeyError:
                    pass
                c_move= chr(ord(c_checking[0])+y)+str(int(c_checking[1])+i)
                try:
                    if self.board.table[c_move] == None or self.board.table[c_move].colour != self.colour:
                        v_moves.append(c_move)
                except KeyError:
                    pass
        self.av_moves = v_moves
        return self.av_moves

    def movement(self, position):
        if position in self.av_moves:
            super().movement(position)
            return 1
        return 0

class Queen(Bishop, Rook):
    name= 'Queen'
    type= 'Q'
    default_img= {0:Image.open(Path('images/queen_b.png')), 1:Image.open(Path('images/queen.png'))}
    def check_pos(self):
        Bishop.check_pos(self)
        B_moves= self.av_moves
        Rook.check_pos(self)
        self.av_moves.extend(B_moves)
        return self.av_moves



class Pawn(Piece):
    name= 'Pawn'
    type= 'P'
    default_img= {0:Image.open(Path('images/peon_b.png')), 1:Image.open(Path('images/peon.png'))}
#The next 2 complex functions define the validity of a move in pawns
#WARNING= Heavy use of if statements ahead
    @staticmethod
    def w_move(initial, table, lm):
        p_m= [1, -1]
        v_moves= []
        en_peassant= ""
        c_checking= initial[0]+str(int(initial[1])+1)
        if table[c_checking] == None:
            v_moves.append(c_checking)
            if initial[1] == '2':
                c_checking= initial[0]+str(int(initial[1])+2)
                if table[c_checking] == None:
                    v_moves.append(c_checking)
        for x in p_m:
            c_checking= chr(ord(initial[0])+x)+str(int(initial[1])+1)
            if table.setdefault(c_checking, None) != None and table[c_checking].colour == 0:
                v_moves.append(c_checking)
            en_p= chr(ord(initial[0])+x)+initial[1]
            if initial[1] == '5' and  table.setdefault(en_p, None) != None and table[en_p] == lm and table[en_p].type == 'P' and table[en_p].colour == 0 and table[en_p].last_movement == en_p[0]+'7':
                en_peassant= [c_checking, en_p]
        return [v_moves, en_peassant]

    @staticmethod
    def b_move(initial, table, lm):
        p_m= [1, -1]
        v_moves= []
        en_peassant= ""
        c_checking= initial[0]+str(int(initial[1])-1)
        if table[c_checking] == None:
            v_moves.append(c_checking)
            if initial[1] == '7':
                c_checking= initial[0]+str(int(initial[1])-2)
                if table[c_checking] == None:
                    v_moves.append(c_checking)
        for x in p_m:
            c_checking= chr(ord(initial[0])+x)+str(int(initial[1])-1)
            if table.setdefault(c_checking, None) != None and table[c_checking].colour == 1:
                v_moves.append(c_checking)
            en_p= chr(ord(initial[0])+x)+initial[1]

            if initial[1] == '4' and table.setdefault(en_p, None) != None and table[en_p] == lm and table[en_p].type == 'P' and table[en_p].colour == 1 and table[en_p].last_movement == en_p[0]+'2':
                en_peassant= [c_checking, en_p]
        return [v_moves, en_peassant]

    al_forw= {
    1: w_move.__func__,
    0: b_move.__func__
    }
    promote= {
    'Q': Queen,
    'N': Knight,
    'R': Rook,
    'B': Bishop
    }

    def check_pos(self):
        self.av_moves= Pawn.al_forw[self.colour](self.position, self.board.table, self.board.lm_piece)
        re= self.av_moves[0]
        if self.av_moves[1] != "":
            re.append(self.av_moves[1][0])
        return re

    def movement(self, position):
        if position in self.av_moves[0]:
            super().movement(position)
            if position[1] == '1' or position[1]== '8':
                try:
                    selection= self.board.promotion_choosing()
                except Exception as e:
                    print(e)
                return self.promotion(selection)
            return 1
        try:
            if position in self.av_moves[1][0]:
                super().movement(position, en_p=self.av_moves[1][1])
                return 1
        except IndexError:
            pass
        return 0

    def promotion(self, selection):
        if selection != 1:        
            self.board.pieces[self.colour][selection].append(self.promote[selection](self.position, self.colour, self.board))
            self.board.pieces[self.colour]['P'].remove(self)
        return 1
class King(Piece):
    name= 'King'
    type= 'K'
    default_img= {0:Image.open(Path('images/king_b.png')), 1:Image.open(Path('images/king.png'))}
    def check_pos(self):
        p_m= [1, -1]
        v_moves = []
        for x in p_m:
            for i in p_m:
                c_checking = chr(ord(self.position[0])+x)+str(int(self.position[1])+i)
                try:
                    if self.board.table[c_checking] == None or self.board.table[c_checking].colour != self.colour:
                        v_moves.append(c_checking)
                except KeyError:
                    pass
            c_checking= [chr(ord(self.position[0])+x)+self.position[1], self.position[0]+str(int(self.position[1])+x)]
            for x in c_checking:
                try:
                    if self.board.table[x] == None or self.board.table[x].colour != self.colour:
                        v_moves.append(x)
                except KeyError:
                    pass
        self.av_moves = v_moves
        return self.av_moves
    def movement(self, position):
        if position in self.av_moves:
            super().movement(position)
            return 1
        return 0

class Game_Chess():
    turn_dict={'w': 1, 'b': 0}
    def __init__(self, promotion_func=cli_promotion, use_imgs=True):
        self.turn= 1
        self.n_turn= 0
        self.board= Board(promotion_func)
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
        numbah= self.board.pieces[self.turn]['K'][0].position[1]
        if self.board.pieces[self.turn]['K'][0].last_movement == None:
            if move == 'OO':
                if self.board.pieces[self.turn]['R'][1].last_movement == None:
                    if self.board.table['f'+numbah] == None and self.board.table['g'+numbah] == None:
                        moves= self.board.check_moves(self.n_turn)
                        if 'f'+numbah not in moves and 'g'+numbah not in moves:
                            self.board.pieces[self.turn]['K'][0].av_moves.append('g'+numbah)
                            self.board.pieces[self.turn]['R'][1].av_moves.append('f'+numbah)
                            self.board.pieces[self.turn]['K'][0].movement('g'+numbah)
                            self.board.pieces[self.turn]['R'][1].movement('f'+numbah)
                            return 1

            elif move == 'OOO':
                if self.board.pieces[self.turn]['R'][0].last_movement == None:
                    if self.board.table['d'+numbah] == None and self.board.table['c'+numbah] == None and self.board.table['b'+numbah] == None:
                        moves= self.board.check_moves(self.n_turn)
                        if 'd'+numbah not in moves and 'c'+numbah not in moves and 'b'+numbah not in moves:
                            self.board.pieces[self.turn]['K'][0].av_moves.append('c'+numbah)
                            self.board.pieces[self.turn]['R'][0].av_moves.append('d'+numbah)
                            self.board.pieces[self.turn]['K'][0].movement('c'+numbah)
                            self.board.pieces[self.turn]['R'][0].movement('d'+numbah)
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
        imported_turn= self.__class__.turn_dict[fen_notation[1]]
        rows= board.split('/')[::-1]
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
        if imported_turn != self.turn:
            self.turn_change()
        self.imported = True
        self.player_and_turn_desired = player_and_turn_desired
        return

    def correct_playerturn(self):
        player= self.player_and_turn_desired[0]
        turn_desired= self.__class__.turn_dict[self.player_and_turn_desired[1]]
        if self.players[turn_desired] != player:
            self.players= self.players[::-1]


importing_pieces_dict= {
    'P': Pawn,
    'B': Bishop,
    'Q': Queen,
    'K': King,
    'R': Rook,
    'N': Knight
}