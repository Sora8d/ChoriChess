from engine_logics.game_objects import Game_P_Chess, Game_Bot_Chess
from engine_logics.session_manager import ro_manager
import time
#TODO
#Finish bot, now bugged...
    

#Games and saved stuff, for GROUP GAMES
class Chess_Bot_Handler(ro_manager):
    def __init__(self, telegrambot):
        super().__init__()
        self.telegrambot = telegrambot
        self.type_games = {0:Game_P_Chess, 1:Game_Bot_Chess}

    def single_player_t(self, *args, **kwargs):
        room= self.create_room(kwargs['ef_id'], 'singleplayer')
        self.put_users(kwargs['user']['first_name'],kwargs['ef_id'], kwargs['user']['id'], room, 0)
        self.put_users(kwargs['user']['first_name'],kwargs['ef_id'], kwargs['user']['id'], room, 0)
        return [str(self.room_members[room]['Board'])]

    def multiplayer_t(self, *args, **kwargs):
        room= self.create_room(kwargs['ef_id'], kwargs['type_chat'])
        self.put_users(kwargs['user']['first_name'],kwargs['ef_id'], kwargs['user']['id'], room, 0)
        return ['Share this token with whoever you want to play', room]

    def join_t(self, *args, **kwargs):
        self.put_users(kwargs['user']['first_name'],kwargs['ef_id'], kwargs['user']['id'], kwargs['token'], 0)
        return ['Game started, Players: \n'+ self.room_members[kwargs['token']]['Board'].players[1][0] + " is white.\n" + self.room_members[kwargs['token']]['Board'].players[0][0] + ' is black']

    def bot_t(self, *args, **kwargs):
        room= self.create_room(kwargs['ef_id'], 'singleplayer')
        self.put_users(kwargs['user']['first_name'],kwargs['ef_id'], kwargs['user']['id'], room, 1)
        return [str(self.room_members[room]['Board'])]

    def create_room(self, id, type_chat):
        self.rooms_list.append('GC'+str(time.time()))
#Board will later be the game object, Private is an option for when i wanna add a game queue, chat_id is the id of the chat that is later passed to the game,
#Ids is a set of the ids of the players, essential to play through Chorichess without a group.
        self.room_members[self.rooms_list[-1]]= {'Board':'', 'Players':[], 'Type': type_chat, 'chat_id': id, 'ids': set()}
        return self.rooms_list[-1]

    def put_users(self, username, sid, user_id, room, bot_nobot):
        try:
            self.members[sid] == {}
        except KeyError:
            self.members[sid] = {}
        self.members[sid][user_id]= []
        self.members[sid][user_id].append(username)
        self.members[sid][user_id].append(room)
        self.room_members[room]['Players'].append([username, user_id])
        self.room_members[room]['ids'].add(user_id)
        if self.room_members[room]['Board'] == '':
           self.room_members[room]['Board'] = self.type_games[bot_nobot](self.room_members[room]['chat_id'], self.room_members[room]['Type'], self.telegrambot)
        game = self.room_members[room]['Board']
        game.add_player([username, user_id])
        if len(game.players) == 2:
            game.startgame()
        return room