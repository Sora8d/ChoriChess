import sqlite3
from sqlite3 import Error
import time
from pathlib import Path
from config import Config

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
CREATE TABLE IF NOT EXISTS games (
    id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
    gameID TEXT NOT NULL UNIQUE,
    turns TEXT,
    white_playerID INTEGER NOT NULL,
    black_playerID INTEGER NOT NULL,
    CONSTRAINT fk_white_user_id 
    FOREIGN KEY(white_playerID) REFERENCES users(id),
    CONSTRAINT fk_black_user_id
    FOREIGN KEY(black_playerID) REFERENCES users(id)
)
"""

create_history_games_table="""
CREATE TABLE IF NOT EXISTS games (
    id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
    gameID TEXT NOT NULL UNIQUE,
    turns TEXT,
    white_playerID INTEGER NOT NULL,
    black_playerID INTEGER NOT NULL,
    winner INTEGER NOT NULL,
    CONSTRAINT fk_white_user_id 
    FOREIGN KEY(white_playerID) REFERENCES users(id),
    CONSTRAINT fk_black_user_id
    FOREIGN KEY(black_playerID) REFERENCES users(id)
)
"""



#To avoid data corruption
def synchronity_wrapper(func):
    def wrapper(self, *args, **kwargs):
        while self.in_use:
            time.sleep(0.1)
        self.in_use= True
        result=func(self, *args,*kwargs)
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
            print('Connection done')
        except Error as e:
            raise e
        self.connection= connection
        self.connection.row_factory= dict_factory

    @synchronity_wrapper
    def execute_query(self, *query):
        connection= self.connection
        cursor= connection.cursor()
        try:
            cursor.execute(*query)
            connection.commit()
            print("Query executed succesfully")
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
        INSERT INTO games (gameID, white_playerID, black_playerID, state) VALUES (?, ?, ?, ?);
        """
        cursor= self.execute_query(query, game)
        return cursor.lastrowid

    def search_game_by_gameID(self, id):
        query="""
        SELECT * FROM games WHERE gameID=?;
        """
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

def telegram_database_decorator(func):
    def wrapper(*args, **kwargs):
        print('running')
        telegram_id= args[0].message.from_user['id']
        default_username= args[0].message.from_user['first_name']
        search= ChoriChessDB.search_by_telegram_id(telegram_id)
        if search == None:
            ChoriChessDB.insert_user((telegram_id,default_username))
            args[1].bot.send_message(chat_id=telegram_id, text="Wait, i dont have you registered in my notebook.\nNow i have registered you as {}. If you want to change this, please type /change_username X replacing X with your desired username.\nAfter you're finished you can copy and paste the command you sent me before".format(default_username))
            return None
        else:
            result= func(*args, *kwargs)
            return result
    return wrapper