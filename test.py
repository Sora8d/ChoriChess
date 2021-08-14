from PIL import Image
from engine_logics.base_chess import Game_Chess
import time
from debug import func_info
from db_funcs import ChoriChessDB, create_game1_table, create_game2_table
import random

def create_dummy_users():
    dummy_user1=ChoriChessDB.insert_user((123, "ALmendra"))
    dummy_user2= ChoriChessDB.insert_user((1234, "Luisito"))
    return dummy_user1, dummy_user2
def create_dummy_games(d1, d2):
    dummy_games= []
    dummy_games.append(ChoriChessDB.insert_game(("fasdsda", d1, d2, 1)))
    dummy_games.append(ChoriChessDB.insert_game(("TARARA", d2, d1, 0)))

    try:
        dummy_games.append(ChoriChessDB.insert_game("GF12", 301234, 11111, 0))
    except Exception as e:
        print(e)
    for x in dummy_games:
        print(ChoriChessDB.search_game_by_id(x))
        
try:
    d_u1, d_u2=create_dummy_users()
except Exception as e:
    print(e)
ChoriChessDB.execute_query(create_game2_table)

create_dummy_games(d_u1, d_u2)

ChoriChessDB.execute_query("DROP TABLE games;")


#ChoriChessDB.execute_query("DELETE FROM users WHERE id=?", (d_u1,))
ChoriChessDB.execute_query("DELETE FROM users WHERE id=? or id=?", (d_u2,d_u1))