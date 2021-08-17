from PIL import Image
from engine_logics.base_chess import Game_Chess
import time
from debug import func_info
from db_funcs import ChoriChessDB, insert_game, update_game_decorator
import random
from sqlite3 import Error

def testdeco(func):
    def wrapper(*args, **kwargs):
        func(*args, **kwargs)
        print(kwargs != {} and kwargs['test_optional_arg'] == False)
        return
    return wrapper

@testdeco
def test_func(test_optional_arg=True):
    pass



class Test_Chess_Game(Game_Chess):
    def __init__(self):
        self.game_id = random.randint(0,100)
        super().__init__(use_imgs=False)
    @insert_game
    def startgame(self):
        return super().startgame()

    @update_game_decorator
    def move(self, player, move):
        return super().move(player, move)

    @update_game_decorator
    def resign(self, resigner):
        return super().resign(resigner)


def test():
    def clean_database():
        query="""
        DELETE FROM active_games;
        DELETE FROM history_games;
        DELETE FROM users;
        """
        ChoriChessDB.execute_query(query, (), mul_statements=True)

    def create_users():
        players= [['Test1', 1], ['Test2', 2], ['Test3', 3]]
        for player in players:
            ChoriChessDB.insert_user((tuple(player)))
        return players

    def create_games(players: list):
        games= [Test_Chess_Game(), Test_Chess_Game(), Test_Chess_Game()]
        order_of_players= [[players[0],players[1]], [players[1],players[0]], [players[1],players[2]]]
        for game, pair_of_players in zip(games, order_of_players):
            game.add_player(pair_of_players[0])
            game.add_player(pair_of_players[1])
            game.startgame()
        return games

    def search_every_game_of_players(players: list):
        for player in players:
            print(player[0] + ' has these games:\n')
            for game in ChoriChessDB.get_all_active_games_of_user(player[1]):
               print(game)

    try:
        clean_database()
        players= create_users()
        create_games(players)
        search_every_game_of_players(players)
        clean_database()
    except (Exception, Error) as e:
        clean_database()
        print('Database cleaned')
        raise e
if __name__=='__main__':
    test()

