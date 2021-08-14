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
