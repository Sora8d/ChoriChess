from db_funcs import ChoriChessDB
from pathlib import Path
from shutil import rmtree
from engine_logics.game_objects import Game_P_Chess, Game_Bot_Chess, Game_Database_Chess
from engine_logics.session_manager import ro_manager
import time
#TODO
#Finish bot, now bugged...
    

#Games and saved stuff, for GROUP GAMES
class Chess_Bot_Handler(ro_manager):
    @staticmethod
    def start_handler(game):
        if len(game.players['list']) == 2:
            game.startgame()
            return

    @staticmethod
    def import_game(game, fen_notation, player_and_turn_desired):
        game.import_board(fen_notation, player_and_turn_desired)
        return

    def __init__(self):
        super().__init__()
        self.type_games = {0:Game_P_Chess, 1:Game_Bot_Chess, 2:Game_Database_Chess}

    def set_up_telegrambot(self, telegrambot):
        self.telegrambot = telegrambot

    def single_player_t(self, *args, **kwargs):
        room= self.create_room(kwargs['ef_id'], 'singleplayer', 0)
        self.put_users(kwargs['ef_id'], kwargs['user']['id'], room)
        self.put_users(kwargs['ef_id'], kwargs['user']['id'], room)
        return [str(self.room_members[room]['Board'])]

    def multiplayer_t(self, *args, **kwargs):
        room= self.create_room(kwargs['ef_id'], kwargs['type_chat'], 2)
        self.put_users(kwargs['ef_id'], kwargs['user']['id'], room)
        return ['Share this token with whoever you want to play', room]

    def join_t(self, *args, **kwargs):
        try:
            self.put_users(kwargs['ef_id'], kwargs['user']['id'], kwargs['token'])
        except KeyError as e:
            self.telegrambot.bot.sendMessage(chat_id=kwargs['ef_id'], text='Game not found')
            raise e
        return ['Game started, Players: \n'+ self.room_members[kwargs['token']]['Board'].players['list'][1][0] + " is white.\n" + self.room_members[kwargs['token']]['Board'].players['list'][0][0] + ' is black']

    def bot_t(self, *args, **kwargs):
        room= self.create_room(kwargs['ef_id'], 'singleplayer', 1)
        self.put_users(kwargs['ef_id'], kwargs['user']['id'], room)
        return [str(self.room_members[room]['Board'])]

    def create_room(self, id, type_chat, bot_nobot):
        token='GC'+str(time.time())
#Board will later be the game object, Private is an option for when i wanna add a game queue, chat_id is the id of the chat that is later passed to the game,
#Ids is a set of the ids of the players, essential to play through Chorichess without a group.
        self.room_members[token]= {'Board':'', 'Players':[], 'Type': type_chat, 'chat_id': id, 'ids': set()}
        self.room_members[token]['Board'] = self.type_games[bot_nobot](token, self.room_members[token]['chat_id'], self.room_members[token]['Type'], self.telegrambot)
        return token

    def put_users(self, sid, user_id, room):
        try:
            self.members[sid] == {}
        except KeyError:
            self.members[sid] = {}
        username= ChoriChessDB.search_by_telegram_id(user_id)['username']
        self.members[sid][user_id]= []
        self.members[sid][user_id].append(username)
        self.members[sid][user_id].append(room)
        self.room_members[room]['Players'].append([username, user_id])
        self.room_members[room]['ids'].add(user_id)
        game = self.room_members[room]['Board']
        game.add_player([username, user_id])
        return room

    def delete_room(self, gameid, playersid):
        for x in playersid:
            try:
                self.room_members.pop(self.members[gameid].pop(x[1])[1])
            except (IndexError, KeyError):
                continue
        if self.members[gameid] == {}:
            self.members.pop(gameid)
        rmtree(Path('./b_imgs/{}'.format(gameid)))
        pass
