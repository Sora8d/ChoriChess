from PIL import Image
from engine_logics.base_chess import Game_Chess, Pawn

tor = Game_Chess()
tor.add_player('yo')
tor.add_player('el')
# tor.import_board('rnbqkbnr/pp1ppppp/8/2p5/P3P2P/7Q/PPPP1P2/RNBQKBNR w')
# tor.move('yo', 'a4')
tor.startgame()
print(tor.move(tor.players[1], 'a4'))
tor.move(tor.players[0], 'a5')
