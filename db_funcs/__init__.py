import sqlite3
from sqlite3 import Error
import time
from pathlib import Path
from config import Config
import json
from datetime import date

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
    date DATE NOT NULL,
    last_activity DATE,
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
    date DATE NOT NULL,
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
    #General ------------------------------
    def create_connection(self, path):
        connection= None
        try:
            connection= sqlite3.connect(path, check_same_thread=False, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
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
                cursor.executescript(query[0].format_map(query[1]))
                connection.commit()
            else:
                cursor.execute(*query)
                connection.commit()
        except Error as e:
            raise e
        return cursor
    #-----------------------------------------

    #User related --------------------------
    def insert_user(self, user: tuple):
        query="""
        INSERT INTO users (telegramid, username) VALUES (?, ?);
        """
        cursor = self.execute_query(query, user)
        return cursor.lastrowid

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

    def get_all_active_games_of_user(self, telegram_id):
        query="""
        SELECT * FROM active_games WHERE white_playerID=? or black_playerID=?;
        """
        cursor= self.execute_query(query, (telegram_id, telegram_id))
        return cursor.fetchall()
    #----------------------------------------

    #Game related ------------------------
    def insert_game(self, game_id, date, last_activity, players_id_dict, moves, turn):
        query="""
        INSERT INTO active_games (gameID, date, last_activity, white_playerID, black_playerID, moves, turn) VALUES (?, ?, ?, ?, ?, ?, ?);
        """
        cursor= self.execute_query(query, (game_id, date, last_activity, players_id_dict['white'], players_id_dict['black'], moves, turn))
        return cursor.lastrowid

    def search_game_by_gameID(self, id, history_game=False):
        table= "active_games" if not history_game else "history_games"
        query="""
        SELECT * FROM {} WHERE gameID=?;
        """.format(table)
        cursor= self.execute_query(query, (id,))
        return cursor.fetchone()
    
    def update_game(self, game_id, moves_json, turn, last_activity):
        query="""
            UPDATE active_games
            SET moves = ?,
            turn= ?,
            last_activity = ?
            WHERE gameID= ?;
            """
        cursor = self.execute_query(query, (moves_json, turn, last_activity, game_id))
        return cursor.lastrowid

    def store_finished_game(self, game_id, winner):
        query="""
            INSERT INTO history_games (date, gameID, white_playerID, black_playerID, moves, winner)
            SELECT date, gameID, white_playerID, black_playerID, moves, {winner}
            FROM active_games
            WHERE gameID= "{game_id}";
            DELETE FROM active_games
            WHERE gameID= "{game_id}";
            """
        self.execute_query(query, {'game_id': game_id, 'winner': winner}, mul_statements=True)
    #----------------------------------------


ChoriChessDB= DBObject()
ChoriChessDB.create_connection(Path(Config.DATABASE))
ChoriChessDB.execute_query(create_users_table)
ChoriChessDB.execute_query(create_active_games_table)                                                                             
ChoriChessDB.execute_query(create_history_games_table)

def database_user_check(func):
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
        players= {'white':self.players['list'][1][1], 'black':self.players['list'][0][1]}
        current_pos_to_json= '{"0": "'+self.FEN_of_current_pos+'"}'
        date_today= date.today()
        ChoriChessDB.insert_game(self.game_id, date_today, date_today, players, current_pos_to_json, self.turn)
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
            ChoriChessDB.update_game(game_id, moves_info_json, self.turn, date.today())

        if result == 3:
            ChoriChessDB.store_finished_game(game_id, self.winner)
        return result
    return wrapper