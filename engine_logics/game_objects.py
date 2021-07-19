from engine_logics.base_chess import Game_Chess
from engine_logics.stockfish_bot import Bridge_Stock_Chess
import time
import os
from pathlib import Path
from functools import partial

def telegram_promotion(game):
    text= 'Choose the piece you want the Pawn to promote to: \ņ/p Q/B/N/R'
    if game.type != 'private':
        game.updater.bot.sendMessage(chat_id=game.id, text=text)
    else:
        game.updater.bot.sendMessage(chat_id=game.players[game.turn][1], text=text)
    t= 0
    while game.response['selection'] == None and t < 60:
        time.sleep(1)
        t+=1
    selection = game.response['selection']
    game.response['selection'] = None
    return selection

def telegram_bot_promotion(game):
    if game.players[game.turn] == game.player_bot:
        selection = game.response['selection']
        game.response['selection'] = None
        return selection
    else:
        return telegram_promotion(game)

class Game_P_Chess(Game_Chess):
    def __init__(self, n_id, type, telegrambot, promotion_func=telegram_promotion):
        promotion_func_with_self= partial(promotion_func, self)
        super().__init__(promotion_func=promotion_func_with_self)
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
        return state

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

class Game_Bot_Chess(Game_P_Chess):
    def __init__(self, promotion_func=telegram_bot_promotion, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.player_bot = ['StockFish {level}'.format(level= 20)]
        self.add_player(self.player_bot)
        self.stockfish= Bridge_Stock_Chess()
    
    def bot_move(self):
        lm_piece = self.board.lm_piece
        if self.players[self.turn] == self.player_bot:
            if lm_piece == '':
                movement_bot= self.stockfish.move()
            else:
                update= lm_piece.last_movement+lm_piece.position
                self.stockfish.update_board(update)
                movement_bot = self.stockfish.move()
            print(movement_bot)
            if movement_bot == 'e1h1' or movement_bot == 'e8h8':
                movement= 'OO'
            elif movement_bot == 'e1a1' or movement_bot == 'e8a8':
                movement= 'OOO'
            else:
                piece_pos= movement_bot[0:2]
                move= movement_bot[2:]
                piece = self.board.table[piece_pos].type if self.board.table[piece_pos].name != 'Pawn' else ''
                movement= piece+move
            state = self.move(self.player_bot, movement)
            if state != 0 or state != 4:
                 self.stockfish.update_board(movement_bot)
                 print('Bot made move ev. okay')
        return
        

    def startgame(self):
        super().startgame()
        self.bot_move()

    def move_handler(self, state, msg):
        super().move_handler(state, msg)
        self.bot_move()