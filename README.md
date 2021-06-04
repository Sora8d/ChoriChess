Chorichess!
This is a TelegramBot that creates and handles Chess games between players,
you can also play by yourself!

Guide:

roclasses.py= Its a "session" ro_manager object, also in FAIF, helps creating rooms and
all the user handling.

chess.py= My own chess logic, using a Game_Chess object that has the board, and pawns.
By itself it is fully playable on Python shell.

chess_bot.py= Here everything comes together, it contains the Telegram Bot, its commands,
and modified versions of ro_manager object and Game_Chess object to suit the bot accordingly. 
