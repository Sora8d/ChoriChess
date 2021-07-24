from PIL import Image
from engine_logics.base_chess import Game_Chess, Pawn

tor = Game_Chess()
tor.add_player('yo')
tor.add_player('el')
tor.import_board('rnbqkbnr/pppppppp/8/8/8/PPPPPPPP/8/RNBQKBNR w', ['yo', 'w'])
# tor.move('yo', 'a4')
tor.startgame()
print(tor.move(tor.players[1], 'a4'))
tor.move(tor.players[0], 'a5')

