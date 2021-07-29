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

    def movement(self, position):
        self.board.table[self.position] = None
        n_p= self.board.table[position]
        if n_p != None:
            n_p.destroy()
        self.board.table[position] = self
        self.last_movement= self.position
        self.position = position
        self.board.lm_piece= self
        self.board.en_peassant= False
        return

    def destroy(self):
        self.board.table[self.position] = None
        self.board.pieces[self.colour][self.type].remove(self)
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

def str_plus_int(stringg, intteger):
    return str(int(stringg)+intteger)

class Pawn(Piece):
    name= 'Pawn'
    type= 'P'
    default_img= {0:Image.open(Path('images/peon_b.png')), 1:Image.open(Path('images/peon.png'))}
    colour_dict= {
        1 : [1, '2'],
        0: [-1, '7']
    }

    promote= {
    'Q': Queen,
    'N': Knight,
    'R': Rook,
    'B': Bishop
    }

    def all_moves(self):
        table= self.board.table
        initial_pos= self.position
        v_moves = []
        direction= Pawn.colour_dict[self.colour][0]
        c_checking= initial_pos[0]+str_plus_int(initial_pos[1],direction)
        if table[c_checking] == None:
                v_moves.append(c_checking)
                if initial_pos[1] == Pawn.colour_dict[self.colour][1]:
                    c_checking= initial_pos[0]+str_plus_int(initial_pos[1],direction*2)
                    if table[c_checking] == None:
                        v_moves.append(c_checking)
        for x in [1, -1]:
            c_checking= chr(ord(initial_pos[0])+x)+str_plus_int(initial_pos[1],direction)
            if (table.setdefault(c_checking, None) != None and table[c_checking].colour != self.colour) or (self.board.en_peassant == c_checking and self.board.lm_piece.colour != self.colour):
                    v_moves.append(c_checking)
        return v_moves


    def check_pos(self):
        self.av_moves= self.all_moves()
        return self.av_moves

    def movement(self, position):
        if position in self.av_moves:
            en_p = False
            if int(self.position[1])-int(position[1]) in [2, -2]:
                en_p=self.position[0]+str_plus_int(self.position[1], Pawn.colour_dict[self.colour][0])
            elif self.board.en_peassant == position:
                self.board.lm_piece.destroy()            
            super().movement(position)
            self.board.en_peassant= en_p
            if position[1] == '1' or position[1]== '8':
                try:
                    selection= self.board.promotion_choosing()
                except Exception as e:
                    print(e)
                return self.promotion(selection)
            return 1

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
