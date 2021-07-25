from pathlib import Path
from PIL import Image




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
