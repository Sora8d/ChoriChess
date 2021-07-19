from PIL import Image
from engine_logics.base_chess import Game_Chess, Pawn

tor = Game_Chess()
tor.add_player('yo')
tor.add_player('el')
# tor.import_board('rnbqkbnr/pp1ppppp/8/2p5/P3P2P/7Q/PPPP1P2/RNBQKBNR w')
# tor.move('yo', 'a4')

tor.import_board('rnbqkbnr/pp1ppppp/8/2p5/4P2P/7Q/PPPP1P2/RNBQKBNR w')

print(tor.move('yo', 'a4'))
print(tor.board.table)
#tor.move(tor.players[1], 'a4')
#tor.move(tor.players[0], 'b5')
#tor.move(tor.players[1], 'b5')
#tor.move(tor.players[0], 'a5')
#tor.move(tor.players[1], 'b6')
#tor.move(tor.players[0], 'a4')
#tor.move(tor.players[1], 'b7')
#tor.move(tor.players[0], 'a3')
#tor.move(tor.players[1], 'a8')

# def partial_try( game, object):
#     print(game)
#     print(object.presence)

# class RTA():
#     def __init__(self):
#         partial_try_with_self= partial(partial_try, self)
#         RDA(partial_try_with_self)
# class RDA():
#     presence="big"
#     def __init__(self, func_to_test):
#         func_to_test(self)

# RTA()
