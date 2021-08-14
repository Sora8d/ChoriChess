from pathlib import Path
from db_funcs import ChoriChessDB

def insert_user_db(update, context):
    ChoriChessDB.insert_user((update.message.from_user['id'], update.message.from_user['first_name']))

def find_me_db(update, context):
    print(ChoriChessDB.search_by_telegram_id((update.message.from_user['id'])))

def change_username_db(update, context):
    id=update.message.from_user['id']
    new_username= " ".join(context.args)
    ChoriChessDB.change_username(new_username,(id,))
    context.bot.send_message(chat_id=id, text='Your new name is {}'.format(new_username))

