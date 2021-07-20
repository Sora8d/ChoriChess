2.3 (20/07/2021 18:00):
    Changes:

    1- Fixed critical bug concerning promoting, going back to main branch.

    2- Importing boards is now possible through FEN notation in telegram games and bot games.

    3- Now that importing boards is possible, testing the bot in specific situations with bots is easier.

    TODO:

    - Make bots able to decide between multiple pieces and also to promote.
    - Divide further the components.

2.2 (18/07/2021 23:00):
    Changes:

    1- Updated and fixed form of promoting. Have yet to test.

    2- Added basic option to import boards, not in telegram games yet.
    
2.1 (18/07/2021):
    Changes:
    
    1- Transformed the structure into packages. Further dividing files.
    
    2- Gamemode against a stockfish bot added.

    3- Fixed logs, now basic logging is available. 

    4- Modified config file to use environmental variables. 

    modules added= stockfish, python-dotenv.

    TODO:
    -Fix promotions, right now doesnt work in any gamemode. 
    -Test bot thoroughly,  specially promotions and castling.
    -Add bot levels, different difficulties. 
    -Fix test.py, create actual tests.
    -Leave more comments.


2.0 (15/07/2021):
    Changes:

    1- Divided chess_bot into chess_bot and chori_bot, the second now cointaining the telegram bot while the telegram-ready chess remains in the chess_bot.

    2- In chess, now move_handler is the main messaging function instead of img_s, that now just creates and saves images. This function is also used in the telegram bot, changed in Game_Bot_Chess to send telegram messages. 

    3- Also in chess, players are added in their own function instead of through __init__.

    4- Removed global variable 'response' and added it into the Game_Bot_Chess to keeps thing local and avoid possible problems between simultaneus games. 


1.0 (06/06/2021):
    Changes:

    1- Now 'type' is part of the object 'Board' and more messages are sent from inside 'Board' methods.

    2- Multiple changes to the methods 'img_s' and 'mul_pieces' in the 'Board' object, followed by changes to the function 'move' in the bot

    3- Changes to the function 'chess_g' replacing the way it identifies games.

    4- Now game sends unique messages to Black and White
    players, only in games played through the bot chat.

    -line 42, 45 Type and type_chat instead of Private

    -line 60, see point 1.


    Cambios:

    1- Ahora 'type' es parte del objeto 'Board' y mas mensajes desde este objeto seran enviados dentro de los metodos de "Board"

    2- Multiples cambios a los metodos 'img_s', 'mul_pieces' del objeto 'Board', seguidos de cambios a la función de 'move' dentro del bot.

    3- Cambios a la función de 'chess_g' reemplazando la forma de identificar el juego.

    4- Ahora el juego envia mensajes unicos a Blancas y Negras, solo en juegos que usan el chat del bot.

    -linea 42 y 45, remplazando 'Private' por 'Type' y 'type_chat'
    -linea 60, mirar punto 1.
