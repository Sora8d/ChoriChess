from engine_logics.chess_s_manager import Chess_Bot_Handler
from engine_logics.game_objects import Game_Handlers
from telegram.ext.dispatcher import run_async
from db_funcs import telegram_database_decorator

CBH= Chess_Bot_Handler()
chess_g_dict={
'singleplayer': CBH.single_player_t,
'invite': CBH.multiplayer_t,
'join': CBH.join_t,
'bot': CBH.bot_t,
}
Game_Handlers[1]= CBH


def master(update, context, action):
    #Sends the creation command to a dict that passes it to the proper handler object
    res= chess_g_dict[action[0]](user=update.message.from_user, token=action[-1], ef_id=update.effective_chat.id, type_chat=update.effective_chat.type)
    room= CBH.room_members[CBH.members[update.effective_chat.id][update.message.from_user['id']][1]]
    game= room['Board']
    return game, res

#This checks who to send the starting message
def messagegames(type, game, res, id, context):
    if type != 'invite':
        game.move_handler(2, res[0])
    else:
        #In multiplayer the game doesnt start inmediately, so it shouldnt send the board picture
        #Plus, it sends the invitation to the only person there
        context.bot.send_message(chat_id=id, text=res[1])
        context.bot.send_message(chat_id=id, text=res[0])
    return game

@telegram_database_decorator
def chess_g(update, context):
    game, res= master(update, context, context.args)
    CBH.start_handler(game)
    messagegames(context.args[0], game, res, update.effective_chat.id, context)


@run_async
def move_g(update, context):
    action = context.args
    try:
        room= CBH.room_members[CBH.members[update.effective_chat.id][update.message.from_user['id']][1]]
    except KeyError as e:
        context.bot.send_message(chat_id=update.effective_chat.id, text='You are not playing any games in this chat')
        raise e
    game= room['Board']
    username= CBH.members[update.effective_chat.id][update.message.from_user['id']][0]
    res= game.move([username, update.message.from_user['id']], action[0])

def choose_g(update, context):
    room= CBH.room_members[CBH.members[update.effective_chat.id][update.message.from_user['id']][1]]
    game= room['Board']
    game.response['selection']= context.args[0]
    return

def resign_g(update, context):
    room= CBH.room_members[CBH.members[update.effective_chat.id][update.message.from_user['id']][1]]
    game= room['Board']
    username= CBH.members[update.effective_chat.id][update.message.from_user['id']][0]
    res=game.resign([username, update.message.from_user['id']])

@telegram_database_decorator
def import_g(update, context):
    game, res= master(update, context, context.args[4:])
    action= context.args
    username= CBH.members[update.effective_chat.id][update.message.from_user['id']][0]
    user_id= update.message.from_user
    CBH.import_game(game, " ".join(action[0:4]), [[username, user_id['id']],action[-1]]) if len(action) == 6 else CBH.import_game(game, " ".join(action[0:4]), [[username, user_id['id']]])
    CBH.start_handler(game)
    messagegames(context.args[4], game, res, update.effective_chat.id, context)
