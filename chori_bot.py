from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.ext.utils.promise import Promise
from telegram.ext.dispatcher import run_async
from config import Config
import logging
import time
import telegram
from pathlib import Path
import os
from chess_bot import Chess_Bot_Handler, Game_Bot_Chess

updater = Updater(token=Config.TOKEN, use_context=True)
dispatcher= updater.dispatcher


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
    "/c_n invite"
    To join a game use the next command, replace TOKEN with the token you've been given
    /c_n join TOKEN
    Once in a game you move by typing "/move MOVEMENT", example /move a4, you dont use x to eat pieces, for pawns you just type the move alone, to move other pieces you follow usual notation. 
    You can resign by typing "/resign"
    ''')
def ayuda(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='''Hola, soy tu choribot, puedes seleccionar un modo de juego con:
    "/c_n singleplayer"
    o
    "/c_n invite"
    Para ingresar a un juego se usa el siguiente comando, remplazando TOKEN por el codigo que te hayan compartido. 
    "/c_n join TOKEN"
    Una vez en un juego, te mueves con "/move MOVEMENT", poe ejemplo /move a4, no usas x para comer piezas, para mover peones pones solamente la posición en el tablero, para mover otras piezas solo mueves notación usual. 
    Puedes resignear escribiendo "/resign"
    ''')

help_handler= CommandHandler('help', help)
ayuda_handler= CommandHandler('ayuda', ayuda)
dispatcher.add_handler(help_handler)
dispatcher.add_handler(ayuda_handler)

CBH= Chess_Bot_Handler(updater)
chess_g_dict={
'singleplayer': CBH.single_player_t,
'invite': CBH.multiplayer_t,
'join': CBH.join_t
}

def chess_g(update, context):
    action = context.args
    #Sends the creation command to a dict that passes it to the proper handler object
    res= chess_g_dict[action[0]](user=update.message.from_user, token=action[-1], ef_id=update.effective_chat.id, type_chat=update.effective_chat.type)
    room= CBH.room_members[CBH.members[update.effective_chat.id][update.message.from_user['id']][1]]
    game= room['Board']
#This checks who to send the starting message
    if action[0] != 'invite':
        game.move_handler(2, res[0])
    else:
        #In multiplayer the game doesnt start inmediately, so it shouldnt send the board picture
        #Plus, it sends the invitation to the only person there
        print(game)
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
    room= CBH.room_members[CBH.members[update.effective_chat.id][update.message.from_user['id']][1]]
    game= room['Board']
    game.response['selection']= int(context.args[0])
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
