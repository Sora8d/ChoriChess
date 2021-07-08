from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.ext.utils.promise import Promise
from telegram.ext.dispatcher import run_async
from config import Config
import logging
from chess import Game_Chess
from roclasses import ro_manager
import time
import telegram
from pathlib import Path
import os
#TODO
#Make more than 1 current image so multiple games dont overlap
#Add a mode to play through Chorichess ----- Fix this, needs a better way to handle id choices
#Give a unique message to black and white players ---- Improved




response= {'selection': None}
updater = Updater(token=Config.TOKEN, use_context=True)
dispatcher= updater.dispatcher
#Games and saved stuff, for GROUP GAMES
class Chess_Bot_Handler(ro_manager):

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
        if len(self.room_members[room]['Players']) == 2:
            self.room_members[room]['Board']= Game_Bot_Chess(self.room_members[room]['chat_id'], self.room_members[room]['Type'], self.room_members[room]['Players'])
            self.room_members[room]['Board'].startgame()
        return room


class Game_Bot_Chess(Game_Chess):
    def __init__(self, n_id, type, *args,**kwargs):
        super().__init__(*args, **kwargs)
        #self.id is a var that saves the id of the chat it belongs, that way in case of mul_pieces, it can send a message so the player picks (it will only be used in group chats, in matches through Chorichess it isnt needed)
        self.id= n_id
        self.type= type
        print(self.players)

    def img_s(self, state, msg):
        invert_n= [7,6,5,4,3,2,1,0]
        if state != 0 and state != 4:
            self.board.c_img = self.board.b_img.copy()
            for x in self.board.pieces:
                for i in self.board.pieces[x]:
                    for z in self.board.pieces[x][i]:
                        self.board.c_img.paste(z.img, (128*(ord(z.position[0])-97), 128*(invert_n[int(z.position[1])-1])), z.img)
            try:
                os.mkdir(Path('b_imgs/{}'.format(self.id)))
            except Exception:
                pass
            self.board.c_img.save(Path('b_imgs/{}/c_move.png'.format(self.id)))
            if state == 5:
                if self.type != 'private':
                    updater.bot.sendMessage(chat_id=self.id, text=msg)
                else:
                    updater.bot.sendMessage(chat_id=self.players[self.n_turn][1], text=msg)
            else:
                if self.type != 'private':
                    updater.bot.send_photo(chat_id=self.id, photo=open(Path('b_imgs/{}/c_move.png'.format(self.id)), 'rb'))
                    updater.bot.send_message(chat_id=self.id, text=msg)
                else:
                    for x in self.players:
                        updater.bot.sendPhoto(chat_id=x[1], photo=open(Path('b_imgs/{}/c_move.png'.format(self.id)), 'rb'))
                        updater.bot.sendMessage(chat_id=x[1], text=msg)
                    updater.bot.sendMessage(chat_id=self.players[self.turn][1], text='Your turn!')
        elif state == 0:
            print(msg)
            if self.type != 'private':
                updater.bot.sendMessage(chat_id=self.id, text=msg)
            else:
                updater.bot.sendMessage(chat_id=self.players[self.turn][1], text=msg)
        return [state, msg]


    def mul_pieces(self, quant, response=response):
        text= ''
        for x in range(len(quant)):
            text+=str(x)+': '+ quant[x].type + ' in ' +quant[x].position+'\n'
        text += 'Input /sel followed by the number of the piece u want to move'
        if self.type != 'private':
            updater.bot.sendMessage(chat_id=self.id, text=text)
        else:
            updater.bot.sendMessage(chat_id=self.players[self.turn][1], text=text)
        t= 0
        while response['selection'] == None and t < 60:
            time.sleep(1)
            t+=1
        selection = response['selection']
        response['selection'] = None
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
        return self.img_s(3, "{} resigned, {} wins".format(resigner[0], self.players[self.winner][0]))





logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='''
    If you need instructions just type "/help"

    Si necesitas instrucciones escribe "/ayuda"
    ''')

start_handler= CommandHandler('start', start)
dispatcher.add_handler(start_handler)

def help(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='''Hello, i am your choribot, you can choose gamemode with either
    "/c_n singleplayer"
    or
    "/c_n multiplayer"
    To join a game use the next command, replace TOKEN with the token you've been given
    /c_n join TOKEN
    Once in a game you move by typing "/move MOVEMENT", example /move a4, you dont use x to eat pieces, for pawns you just type the move alone, to move other pieces you follow usual notation. 
    You can resign by typing "/resign"
    ''')
def ayuda(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='''Hola, soy tu choribot, puedes seleccionar un modo de juego con:
    "/c_n singleplayer"
    o
    "/c_n multiplayer"
    Para ingresar a un juego se usa el siguiente comando, remplazando TOKEN por el codigo que te hayan compartido. 
    "/c_n join TOKEN"
    Una vez en un juego, te mueves con "/move MOVEMENT", poe ejemplo /move a4, no usas x para comer piezas, para mover peones pones solamente la posición en el tablero, para mover otras piezas solo mueves notación usual. 
    Puedes resignear escribiendo "/resign"
    ''')

help_handler= CommandHandler('help', help)
ayuda_handler= CommandHandler('ayuda', ayuda)
dispatcher.add_handler(help_handler)
dispatcher.add_handler(ayuda_handler)

CBH= Chess_Bot_Handler()
chess_g_dict={
'singleplayer': CBH.single_player_t,
'multiplayer': CBH.multiplayer_t,
'join': CBH.join_t
}

def chess_g(update, context):
    action = context.args
    #Sends the creation command to a dict that passes it to the proper handler object
    res= chess_g_dict[action[0]](user=update.message.from_user, token=action[-1], ef_id=update.effective_chat.id, type_chat=update.effective_chat.type)
    room= CBH.room_members[CBH.members[update.effective_chat.id][update.message.from_user['id']][1]]
    game= room['Board']
#This checks who to send the starting message
    if action[0] != 'multiplayer':
        if game.type == "private":
            for x in game.players:
                context.bot.send_photo(chat_id=x[1], photo=open(Path('b_imgs/{}/c_move.png'.format(game.id)), 'rb'))
                context.bot.send_message(chat_id=x[1], text=res[0])
        else:
            context.bot.send_photo(chat_id=update.effective_chat.id, photo=open(Path('b_imgs/{}/c_move.png'.format(game.id)), 'rb'))
            context.bot.send_message(chat_id=update.effective_chat.id, text=res[0])
    else:
        #In multiplayer the game doesnt start inmediately, so it shouldnt send the board picture
        #Plus, it sends the invitation to the oly person there
        context.bot.send_message(chat_id=update.effective_chat.id, text=res[1])
        context.bot.send_message(chat_id=update.effective_chat.id, text=res[0])

chess_g_handler= CommandHandler('c_n', chess_g)
dispatcher.add_handler(chess_g_handler)

@run_async
def move_g(update, context):
    action = context.args
    print(CBH.members[update.effective_chat.id])
    room= CBH.room_members[CBH.members[update.effective_chat.id][update.message.from_user['id']][1]]
    game= room['Board']
    res= game.move([update.message.from_user['first_name'], update.message.from_user['id']], action[0])

move_g_handler= CommandHandler('move', move_g)
dispatcher.add_handler(move_g_handler)

def choose_g(update, context):
    response['selection']= int(context.args[0])
    return

choose_g_handler= CommandHandler('sel', choose_g)
dispatcher.add_handler(choose_g_handler)

def resign_g(update, context):
    room= CBH.room_members[CBH.members[update.effective_chat.id][update.message.from_user['id']][1]]
    game= room['Board']
    res=game.resign([update.message.from_user['first_name'], update.message.from_user['id']])

resign_g_handler= CommandHandler('resign', resign_g)
dispatcher.add_handler(resign_g_handler)

def test(update, context):
    for x in dir(context.bot):
        print(x)

test_handler= CommandHandler('test', test)
dispatcher.add_handler(test_handler)

if __name__=='__main__':
    updater.start_polling()
    try:
        os.mkdir(Path('./b_imgs'))
    except Exception:
        pass
