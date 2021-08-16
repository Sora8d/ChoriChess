import sqlite3
from sqlite3 import Error
import time
from pathlib import Path
from config import Config
import json

def dict_factory(cursor,row):
    d= {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

create_users_table= """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    telegramid INTEGER NOT NULL UNIQUE,
    username TEXT
    );
    """

create_active_games_table="""
CREATE TABLE IF NOT EXISTS active_games (
    id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
    gameID TEXT NOT NULL UNIQUE,
    turn INTEGER NOT NULL,
    moves TEXT NOT NULL,
    white_playerID INTEGER NOT NULL,
    black_playerID INTEGER NOT NULL,
    CONSTRAINT fk_white_user_id 
    FOREIGN KEY(white_playerID) REFERENCES users(telegramid),
    CONSTRAINT fk_black_user_id
    FOREIGN KEY(black_playerID) REFERENCES users(telegramid)
)
"""

create_history_games_table="""
CREATE TABLE IF NOT EXISTS history_games (
    id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
    gameID TEXT NOT NULL UNIQUE,
    moves TEXT NOT NULL,
    white_playerID INTEGER NOT NULL,
    black_playerID INTEGER NOT NULL,
    winner INTEGER NOT NULL,
    CONSTRAINT fk_white_user_id 
    FOREIGN KEY(white_playerID) REFERENCES users(telegramid),
    CONSTRAINT fk_black_user_id
    FOREIGN KEY(black_playerID) REFERENCES users(telegramid)
)
"""



#To avoid data corruption
def synchronity_wrapper(func):
    def wrapper(self, *args, **kwargs):
        while self.in_use:
            time.sleep(0.1)
        self.in_use= True
        result=func(self, *args,**kwargs)
        self.in_use= False
        return result
    return wrapper



class DBObject():
    def __init__(self):
        self.in_use= False
        pass

    def create_connection(self, path):
        connection= None
        try:
            connection= sqlite3.connect(path, check_same_thread=False)
        except Error as e:
            raise e
        self.connection= connection
        self.connection.row_factory= dict_factory

    @synchronity_wrapper
    def execute_query(self, *query, mul_statements=False):
        connection= self.connection
        cursor= connection.cursor()
        try:
            if mul_statements:
                cursor.executescript(query[0].format(*query[1]))
                connection.commit()
            else:
                cursor.execute(*query)
                connection.commit()
        except Error as e:
            raise e
        return cursor

    def insert_user(self, user):
        query="""
        INSERT INTO users (telegramid, username) VALUES (?, ?);
        """
        cursor = self.execute_query(query, user)
        return cursor.lastrowid

    def insert_game(self, game):
        query="""
        INSERT INTO active_games (gameID, white_playerID, black_playerID, state) VALUES (?, ?, ?, ?);
        """
        cursor= self.execute_query(query, game)
        return cursor.lastrowid

    def search_game_by_gameID(self, id, history_game=False):
        table= "active_games" if not history_game else "history_games"
        query="""
        SELECT * FROM {} WHERE gameID=?;
        """.format(table)
        cursor= self.execute_query(query, (id,))
        return cursor.fetchone()

    def search_by_telegram_id(self, telegram_id):
        query="""
        SELECT * FROM users WHERE telegramid=?;
        """
        cursor= self.execute_query(query, (telegram_id,))
        return cursor.fetchone()

    def change_username(self, username, telegram_id):
        query="""
        UPDATE users
        SET username=?
        WHERE telegramid=?;
        """
        self.execute_query(query, (username, telegram_id))

ChoriChessDB= DBObject()
ChoriChessDB.create_connection(Path(Config.DATABASE))
ChoriChessDB.execute_query(create_users_table)
ChoriChessDB.execute_query(create_active_games_table)
ChoriChessDB.execute_query(create_history_games_table)

def telegram_database_decorator(func):
    def wrapper(*args, **kwargs):
        telegram_id= args[0].message.from_user['id']
        default_username= args[0].message.from_user['first_name']
        search= ChoriChessDB.search_by_telegram_id(telegram_id)
        if search == None:
            ChoriChessDB.insert_user((telegram_id,default_username))
            args[1].bot.send_message(chat_id=telegram_id, text="Wait, i dont have you registered in my notebook.\nNow i have registered you as {}. If you want to change this, please type /change_username X replacing X with your desired username.\nAfter you're finished you can copy and paste the command you sent me before".format(default_username))
            return None
        else:
            result= func(*args, **kwargs)
            return result
    return wrapper

def insert_game(func):
    def wrapper(self):
        result= func(self)
        query="""
        INSERT INTO active_games (gameID, white_playerID, black_playerID, moves, turn) VALUES (?, ?, ?, ?, ?);
        """
        ChoriChessDB.execute_query(query, (self.game_id, self.players['list'][1][1], self.players['list'][0][1], '{}',1))
        print(ChoriChessDB.search_game_by_gameID(self.game_id))
        return result
    return wrapper

def update_game_decorator(func):
    def wrapper(self, player, *args):
        result= func(self,player,*args)
        if result != 0 and result != 4:
            game_id = self.game_id
            turn_number = self.turn_number
            move_notation = self.FEN_of_current_pos
            moves_info =json.loads(ChoriChessDB.search_game_by_gameID(game_id)['moves'])
            moves_info[turn_number]= move_notation
            moves_info_json = json.dumps(moves_info)
            update_query="""
            UPDATE active_games
            SET moves = ?,
            turn= ?
            WHERE gameID= ?;
            """
            ChoriChessDB.execute_query(update_query, (moves_info_json, self.turn ,game_id))
        if result == 3:
            store_finished_game_query="""
            INSERT INTO history_games (gameID, white_playerID, black_playerID, moves, winner)
            SELECT gameID, white_playerID, black_playerID, moves, {}
            FROM active_games
            WHERE gameID= "{}";
            DELETE FROM active_games
            WHERE gameID= "{}";
            """
            cursor = ChoriChessDB.execute_query(store_finished_game_query, (self.winner, game_id, game_id), mul_statements=True)
        return result
    return wrapper