from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.ext.utils.promise import Promise

from config import Config
import logging
from pathlib import Path
import os

from chori_bot_logics.chess_handlers import *
from chori_bot_logics.help_handlers import *
from chori_bot_logics.database_handlers import *


#Set up Bot
updater = Updater(token=Config.TOKEN, use_context=True)
dispatcher= updater.dispatcher


#Set up Chess-sessions Manager
CBH.set_up_telegrambot(updater)

def error_print(e, a, aa):
    print(e, a, aa)
dispatcher.add_error_handler(error_print)

#Logs
try:
    os.mkdir(Path('./logs'))
except Exception:
    pass
logging.basicConfig(filename= './logs/log.log', filemode='a',  format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='''
    If you need instructions just type "/help"

    Si necesitas instrucciones escribe "/ayuda"
    ''')

start_handler= CommandHandler('start', start)
dispatcher.add_handler(start_handler)


#help_bot ------------
help_handler= CommandHandler('help', help)
ayuda_handler= CommandHandler('ayuda', ayuda)
dispatcher.add_handler(help_handler)
dispatcher.add_handler(ayuda_handler)

#database_handlers -----------
insert_user_db_handler= CommandHandler('insertme', insert_user_db)
dispatcher.add_handler(insert_user_db_handler)
find_me_db_handler= CommandHandler('findme', find_me_db)
dispatcher.add_handler(find_me_db_handler)
change_username_db_handler= CommandHandler('change_username', change_username_db)
dispatcher.add_handler(change_username_db_handler)


#chess_handlers ------------
chess_g_handler= CommandHandler('c_n', chess_g)
dispatcher.add_handler(chess_g_handler)

import_g_handler= CommandHandler('import', import_g)
dispatcher.add_handler(import_g_handler)

move_g_handler= CommandHandler('move', move_g)
dispatcher.add_handler(move_g_handler)

choose_g_handler= CommandHandler('sel', choose_g)
dispatcher.add_handler(choose_g_handler)

resign_g_handler= CommandHandler('resign', resign_g)
dispatcher.add_handler(resign_g_handler)

if __name__=='__main__':
    updater.start_polling()
    try:
        os.mkdir(Path('./b_imgs'))
    except Exception:
        pass
