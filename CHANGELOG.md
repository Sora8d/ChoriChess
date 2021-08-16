3.4.2 (15/08/2021):
    Changes:

    1- game table is not divided into active_games and history_games

    2- Games are now succesfully stored in the database, and it updates after every move, storing them in a JSON.

    3- Finished move to notation decorator, changed it to a function instead of a decorator.

    4- Now games save the turn they are in (turn 1, 2, 3, etc), and the token as game_id (the previous id variable has changed to chat_id)

    5- Multiplayer games (the ones that will be stored in the database) now have their own Game object, as to add the database decorators required for storage, other games are not of interest to store.

    TODO:

    1- Move active_games to history_games after someone wins.

    2- Make importing games work properly with the database.

3.4.1 (14/08/2021):
    Changes:

    1- Added a game table.

    2- In process of adding a decorator to save notation of moves for storage purposes.

3.4 (13/08/2021):
    Changes:

    1- Added a lot of ways to handle errors, including 2 herror_handlers funcions for importing, and a custom Exception class inside Game_P_Chess object.

    2- Added a Database system, for now it keeps track of players, giving them the possibility to change usernames.

    3- chori_bot now only activates the functions that are inside chori_bot_logics

    TODO:

    1- Make players able to have more than one active game per chat.

    2- Create Game table.

3.3.2 (09/09/2021):
    Changes:
    
    1- Fixed King bug, also fixed another bug that made the bot incapable of deleting finished games.

3.3.1 (08/08/2021):
    Changes:

    1- Added some Error Handlers regarding not being in a game and inserting a wrong token.

    2- Combined every function that has to do with Response into response_wait.

    TODO:

    1- Add the remaining Error Handlers.

    2- Implement a Database.

    3- Make players able to have more than one game active through Chorichess.

    4- NEW BUG: When in Check, King is unable to move, need to fix.

3.3 (08/08/2021):
    Changes:

    1- Implemented a delete_room function in the manager, and managed to implement it in Chess_P and Chess_Bot games. Now finished games will be deleted.
    2- Substituted a piece of the code in the img_s of Chess_P, now when not playing a private match (where you have two images for black and white players), it uses a list comprehension insted of nested loops.

    TODO:

    1- Add Error Handlers.

    2- Implement a Database.

3.2 (28/07/2021):
    Changes:

    1- Changed the function that checks Pawns movement.
    2- Change way en_peassant works, now its a variable in the Board object, before it was checked in the movement_checker of Pawns.
    3- Changed way of FEN Castling.
    4- Changed way Castling works in the Game_Chess object.  
    5- Made it able to add en_peassant FEN notations
    6- Tested castling with bots, works.
    7- Now bots dont enter a bucle when game ends.

    TODO:

    1- Fix multiple IMGS at end of games. 

    2- Still have to add error handlers.

    3- Still need a way of erasing data after games are done.

3.1 (24/07/2021 21:00):
    Changes:

    1- Correctly implemented Castling notation when importing games.

    2- Further compartmentization of objects, now base chess has a sub-folder with the base board and pieces. 

    TODO:

    Everything of the 3.0 list.

    + Finish adding en_peassant FEN notation

3.0 (23/07/2021 22:20):
    Changes:

    1- Bot is now able to promote and to choose between equal options

    2- Bug encountered, Stockfish will get stuck if u put two pawns one move behind promotion. Need to get more testing.

    3- Other bug. Stockfish 14 breaks with some imported boards. Need more testing, for now Stockfish 13 is being used. 

    TODO:

    1- Yet to test castling with bot.

    2- When a game is over bot will start cycling, need to fix that.

    3- Start adding some error handlers.

    4- Start eliminating done games.

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
