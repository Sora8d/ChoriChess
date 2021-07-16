from chess import Game_Chess
from roclasses import ro_manager
import time
from pathlib import Path
import os
#TODO
#Make more than 1 current image so multiple games dont overlap
#Add a mode to play through Chorichess ----- Fix this, needs a better way to handle id choices
#Give a unique message to black and white players ---- Improved
    

#Games and saved stuff, for GROUP GAMES
class Chess_Bot_Handler(ro_manager):
    def __init__(self, telegrambot):
        super().__init__()
        self.telegrambot = telegrambot

    def single_player_t(self, *args, **kwargs):
        room= self.create_room(kwargs['ef_id'], 'singleplayer')
        self.put_users(kwargs['user']['first_name'],kwargs['ef_id'], kwargs['user']['id'], room)
        self.put_users(kwargs['user']['first_name'],kwargs['ef_id'], kwargs['user']['id'], room)
        return [str(self.room_members[room]['Board'])]

    def multiplayer_t(self, *args, **kwargs):
        room= self.create_room(kwargs['ef_id'], kwargs['type_chat'])
        self.put_users(kwargs['user']['first_name'],kwargs['ef_id'], kwargs['user']['id'], room)
        return ['Share this token with whoever you want to play', room]

    def join_t(self, *args, **kwargs):
        self.put_users(kwargs['user']['first_name'],kwargs['ef_id'], kwargs['user']['id'], kwargs['token'])
        return ['Game started, Players: \n'+ self.room_members[kwargs['token']]['Board'].players[1][0] + " is white.\n" + self.room_members[kwargs['token']]['Board'].players[0][0] + ' is black']

    def create_room(self, id, type_chat):
        self.rooms_list.append('GC'+str(time.time()))
#Board will later be the game object, Private is an option for when i wanna add a game queue, chat_id is the id of the chat that is later passed to the game,
#Ids is a set of the ids of the players, essential to play through Chorichess without a group.
        self.room_members[self.rooms_list[-1]]= {'Board':'', 'Players':[], 'Type': type_chat, 'chat_id': id, 'ids': set()}
        return self.rooms_list[-1]

    def put_users(self, username, sid, user_id, room):
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
            self.room_members[room]['Board']= Game_Bot_Chess(self.room_members[room]['chat_id'], self.room_members[room]['Type'], self.telegrambot)
        game = self.room_members[room]['Board']
        game.add_player([username, user_id])
        if len(self.room_members[room]['Players']) == 2:
            game.startgame()
        return room


class Game_Bot_Chess(Game_Chess):
    def __init__(self, n_id, type, telegrambot):
        super().__init__()
        #self.id is a var that saves the id of the chat it belongs, that way in case of mul_pieces, it can send a message so the player picks (it will only be used in group chats, in matches through Chorichess it isnt needed)
        self.id= n_id
        self.type= type
        self.updater= telegrambot
        self.response= {'selection': None}

    def move_handler(self, state, msg):
        if state != 0 and state !=4:
            self.img_s()
            if state == 5:
                if self.type != 'private':
                    self.updater.bot.sendMessage(chat_id=self.id, text=msg)
                else:
                    self.updater.bot.sendMessage(chat_id=self.players[1][1], text=msg)
                    self.updater.bot.sendMessage(chat_id=self.players[0][1], text=msg)
            else:
                if self.type != 'private':
                    self.updater.bot.sendPhoto(chat_id=self.id, photo=open(Path('b_imgs/{}/c_move.png'.format(self.id)), 'rb'))
                    self.updater.bot.sendMessage(chat_id=self.id, text=msg)
                else:
                    self.updater.bot.sendPhoto(chat_id=self.players[1][1], photo=open(Path('b_imgs/{}/c_move.png'.format(self.id)), 'rb'))
                    self.updater.bot.sendMessage(chat_id=self.players[1][1], text=msg)
                    self.updater.bot.sendPhoto(chat_id=self.players[0][1], photo=open(Path('b_imgs/{}/c_move_black.png'.format(self.id)), 'rb'))
                    self.updater.bot.sendMessage(chat_id=self.players[0][1], text=msg)                    
                if self.type != 'singleplayer' and self.game == 1:
                    if self.type != 'private':
                        self.updater.bot.sendMessage(chat_id=self.id, text='Its {} turn'.format(self.players[self.turn][0]))
                    else:
                        self.updater.bot.sendMessage(chat_id=self.players[self.turn][1], text='Your turn!')
        elif state == 0:
            print(msg)
            if self.type != 'private':
                self.updater.bot.sendMessage(chat_id=self.id, text=msg)
            else:
                self.updater.bot.sendMessage(chat_id=self.players[self.turn][1], text=msg)
        elif state == 4:
            if self.type != 'private':
                self.updater.bot.sendMessage(chat_id=self.id, text=msg)
            else:
                self.updater.bot.sendMessage(chat_id=self.players[self.n_turn][1], text=msg)
        return

    def img_s(self):
        try:
            os.mkdir(Path('b_imgs/{}'.format(self.id)))
        except Exception:
            pass
        invert_n= [7,6,5,4,3,2,1,0]
        self.board.c_img = self.board.b_img.copy()
#This is just one board, with white on bottom. 
        if self.type != 'private':
            for x in self.board.pieces:
                for i in self.board.pieces[x]:
                    for z in self.board.pieces[x][i]:
                        self.board.c_img.paste(z.img, (128*(ord(z.position[0])-97), 128*(invert_n[int(z.position[1])-1])), z.img)
            self.board.c_img.save(Path('b_imgs/{}/c_move.png'.format(self.id)))
#Creates custom boards for black and white players.
        elif self.type == 'private':
            self.board.c_img_black = self.board.b_img.copy()
            for x in self.board.pieces:
                for i in self.board.pieces[x]:
                    for z in self.board.pieces[x][i]:
                        self.board.c_img.paste(z.img, (128*(ord(z.position[0])-97), 128*(invert_n[int(z.position[1])-1])), z.img)
                        self.board.c_img_black.paste(z.img, (128*(ord(z.position[0])-97), 128*(int(z.position[1])-1)), z.img)
            self.board.c_img.save(Path('b_imgs/{}/c_move.png'.format(self.id)))
            self.board.c_img_black.save(Path('b_imgs/{}/c_move_black.png'.format(self.id)))
        return 


    def mul_pieces(self, quant):
        text= ''
        for x in range(len(quant)):
            text+=str(x)+': '+ quant[x].type + ' in ' +quant[x].position+'\n'
        text += 'Input /sel followed by the number of the piece u want to move'
        if self.type != 'private':
            self.updater.bot.sendMessage(chat_id=self.id, text=text)
        else:
            self.updater.bot.sendMessage(chat_id=self.players[self.turn][1], text=text)
        t= 0
        while self.response['selection'] == None and t < 60:
            time.sleep(1)
            t+=1
        selection = self.response['selection']
        self.response['selection'] = None
        if type(selection) != int or len(quant)-1 < selection:
            return 0
        mov= quant[selection]
        return mov

    def resign(self, resigner):
        self.game= 0
        if self.players.index(resigner) == 1:
            self.winner=0
        if self.players.index(resigner) == 0:
            self.winner=1
        return self.move_handler(3, "{} resigned, {} wins".format(resigner[0], self.players[self.winner][0]))