from PIL import Image
from engine_logics.base_chess import Game_Chess
import time
#tor = Game_Chess()
#tor.add_player('yo')
#tor.add_player('el')
#tor.import_board('rnbqkbnr/p1pppppp/8/1pP5/8/8/PPPPPPPP/R3KBNR w KQkq b6', ['yo', 'w'])
#tor.startgame()
#time.sleep(2)
#tor.move(tor.players[1], 'b6')
#
#for x in tor.board.pieces[0]['P']:
#    print(x.position)
#for x in tor.board.pieces[1]['P']:
#    print(x.position)

from stockfish import Stockfish
from config import Config

stocky= Stockfish(Config.STOCKFISH)
stocky.set_skill_level(1)
print(stocky._parameters)
stocky.set_skill_level(5)
print(stocky._parameters)
stocky.set_skill_level(10)
print(stocky._parameters)
stocky.set_skill_level(15)
print(stocky._parameters)
stocky.set_skill_level(20)
print(stocky._parameters)
#for castling tests.
#/import r3k3/8/8/8/8/8/2P1P3/2RKR3 b q -