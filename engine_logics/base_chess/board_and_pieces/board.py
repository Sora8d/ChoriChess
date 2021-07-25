import copy, random
from PIL import Image
from pathlib import Path
from engine_logics.base_chess.board_and_pieces.pieces import Pawn, Rook, King, Bishop, Queen, Knight


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
        self.b_img= Image.open(Path('images/tablero_{}.png'.format(random.randint(1,4))))
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