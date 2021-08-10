from PIL import Image
from engine_logics.base_chess import Game_Chess
import time
from debug import func_info
desired_input= ""
def mock_input(input_func):
    def input_values(*args, **kwargs):
        return args[0][desired_input]
    return input_values
    
        

tor = Game_Chess()
tor.mul_pieces= mock_input(tor.mul_pieces)
tor.add_player('yo')
tor.add_player('el')
tor.import_board("k6r/7p/8/8/8/8/K7/R6R w - -", ['yo', 'w'])
tor.startgame()
tor.board.king_move_check= func_info(tor.board.king_move_check)
desired_input= 1
tor.move('yo', 'Rb1')
tor.move('el', 'Rc8')
tor.move('yo', 'Rb5')
tor.move('el', 'Rc2')
print(tor.board.pieces)



#tor.move('yo', 'Kb1')
#for castling tests.
#/import r3k3/8/8/8/8/8/2P1P3/2RKR3 b q -