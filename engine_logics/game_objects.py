
from db_funcs import insert_game, update_game_decorator
from engine_logics.base_chess import Game_Chess, transform_pos_to_FEN
from engine_logics.stockfish_bot import Bridge_Stock_Chess
import time
import os
from pathlib import Path
from functools import partial

Game_Handlers= {}

def response_wait(game, text):
    if game.type != 'private':
        game.updater.bot.sendMessage(chat_id=game.id, text=text)
    else:
        game.updater.bot.sendMessage(chat_id=game.players['list'][game.turn][1], text=text)
    t= 0
    while game.response['selection'] == None and t < 60:
        time.sleep(1)
        t+=1
    selection = game.response['selection']
    game.response['selection'] = None
    return selection

class Game_P_Chess(Game_Chess):
    def __init__(self, token, n_id, type, telegrambot):
        #self.id is a var that saves the id of the chat it belongs, that way in case of mul_pieces, it can send a message so the player picks (it will only be used in group chats, in matches through Chorichess it isnt needed)
        self.game_id= token
        self.chat_id= n_id
        self.type= type
        self.updater= telegrambot
        self.response= {'selection': None}
        self.turn_number= 0
        super().__init__(promotion_func=self.telegram_promotion)

    def create_exceptions(self):
        class ToMessageError(Exception):
            def __init__(self_of_error):
                self_of_error.updater= self.updater
                self_of_error.players= self.players
            def error(self_of_error, message):
                super().__init__(message)
                if len(self_of_error.players['list']) == 1:
                    self_of_error.updater.bot.sendMessage(chat_id=self_of_error.players['list'][0][1], text=message)
                elif len(self_of_error.players['list']) == 2:
                    self_of_error.updater.bot.sendMessage(chat_id=self_of_error.players['list'][self.turn][1], text=message)
                
                raise self_of_error
        self.error = ToMessageError().error

    def move_handler(self, state, msg):
        if state != 0 and state !=4:
            self.FEN_of_current_pos= transform_pos_to_FEN(self.board, self.turn)
            self.img_s()
            if state == 5:
                if self.type != 'private':
                    self.updater.bot.sendMessage(chat_id=self.chat_id, text=msg)
                else:
                    self.updater.bot.sendMessage(chat_id=self.players['list'][1][1], text=msg)
                    self.updater.bot.sendMessage(chat_id=self.players['list'][0][1], text=msg)
            else:
                if state != 2:
                    self.turn_number += 1
                if self.type != 'private':
                    self.updater.bot.sendPhoto(chat_id=self.chat_id, photo=open(Path('b_imgs/{}/c_move.png'.format(self.chat_id)), 'rb'))
                    self.updater.bot.sendMessage(chat_id=self.chat_id, text=msg)
                else:
                    self.updater.bot.sendPhoto(chat_id=self.players['list'][1][1], photo=open(Path('b_imgs/{}/c_move.png'.format(self.chat_id)), 'rb'))
                    self.updater.bot.sendMessage(chat_id=self.players['list'][1][1], text=msg)
                    self.updater.bot.sendPhoto(chat_id=self.players['list'][0][1], photo=open(Path('b_imgs/{}/c_move_black.png'.format(self.chat_id)), 'rb'))
                    self.updater.bot.sendMessage(chat_id=self.players['list'][0][1], text=msg)                    
                if self.type != 'singleplayer' and self.game == 1:
                    if self.type != 'private':
                        self.updater.bot.sendMessage(chat_id=self.chat_id, text='Its {} turn'.format(self.players['list'][self.turn][0]))
                    else:
                        self.updater.bot.sendMessage(chat_id=self.players['list'][self.turn][1], text='Your turn!')
        elif state == 0:
            if self.type != 'private':
                self.updater.bot.sendMessage(chat_id=self.chat_id, text=msg)
            else:
                self.updater.bot.sendMessage(chat_id=self.players['list'][self.turn][1], text=msg)
        elif state == 4:
            if self.type != 'private':
                self.updater.bot.sendMessage(chat_id=self.chat_id, text=msg)
            else:
                self.updater.bot.sendMessage(chat_id=self.players['list'][self.n_turn][1], text=msg)
        
        if state == 3:
            Game_Handlers[1].delete_room(self.chat_id, self.players['list'])
        return state

    def img_s(self):
        try:
            os.mkdir(Path('b_imgs/{}'.format(self.chat_id)))
        except Exception:
            pass
        invert_n= [7,6,5,4,3,2,1,0]
        self.board.c_img = self.board.b_img.copy()
#This is just one board, with white on bottom. 
        if self.type != 'private':
            [self.board.c_img.paste(z.img, (128*(ord(z.position[0])-97), 128*(invert_n[int(z.position[1])-1])), z.img) for x in self.board.pieces for i in self.board.pieces[x] for z in self.board.pieces[x][i]]
            self.board.c_img.save(Path('b_imgs/{}/c_move.png'.format(self.chat_id)))
#Creates custom boards for black and white players['list'].
        elif self.type == 'private':
            self.board.c_img_black = self.board.b_img.copy()
            for x in self.board.pieces:
                for i in self.board.pieces[x]:
                    for z in self.board.pieces[x][i]:
                        self.board.c_img.paste(z.img, (128*(ord(z.position[0])-97), 128*(invert_n[int(z.position[1])-1])), z.img)
                        self.board.c_img_black.paste(z.img, (128*(ord(z.position[0])-97), 128*(int(z.position[1])-1)), z.img)
            self.board.c_img.save(Path('b_imgs/{}/c_move.png'.format(self.chat_id)))
            self.board.c_img_black.save(Path('b_imgs/{}/c_move_black.png'.format(self.chat_id)))
        return 

#These ones wait for a response from chat. 
    def mul_pieces(self, quant):
        text= ''
        for x in range(len(quant)):
            text+=str(x)+': '+ quant[x].type + ' in ' +quant[x].position+'\n'
        text += 'Input /sel followed by the number of the piece u want to move'
        selection= int(response_wait(self, text))
        if type(selection) != int or len(quant)-1 < selection:
            return 0
        mov= quant[selection]
        return mov

    def telegram_promotion(self):
        text= 'Choose the piece you want the Pawn to promote to: /sel Q/B/N/R'
        selection= response_wait(self, text)
        return selection



class Game_Bot_Chess(Game_P_Chess):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.player_bot = ['StockFish {level}'.format(level= 20)]
        self.add_player(self.player_bot)
        self.stockfish= Bridge_Stock_Chess()
    

    def bot_position_and_piece(self, movement_bot):
        if movement_bot == 'e1g1' or movement_bot == 'e8g8':
            movement= 'OO'
        elif movement_bot == 'e1c1' or movement_bot == 'e8c8':
            movement= 'OOO'
        else:
            piece_pos= movement_bot[0:2]
            move= movement_bot[2:]
            piece = self.board.table[piece_pos].type if self.board.table[piece_pos].name != 'Pawn' else ''
            movement= piece+move
        return movement

    def bot_move(self):
        lm_piece = self.board.lm_piece
        if self.players['list'][self.turn] == self.player_bot:
            if lm_piece == '':
                movement_bot= self.stockfish.move()
            else:
                update= lm_piece.last_movement+lm_piece.position
                self.stockfish.update_board(update)
                movement_bot = self.stockfish.move()
            
            print(movement_bot)
            if len(movement_bot) > 4:
                self.response['selection'] = movement_bot[-1].upper()
            self.response['position'] = movement_bot[0:2]
            movement= self.bot_position_and_piece(movement_bot[0:4])

            state = self.move(self.player_bot, movement)

            if state != 0 or state != 4:
                 self.stockfish.update_board(movement_bot)
        return
        

    def startgame(self):
        super().startgame()

    def move_handler(self, state, msg):
        _s= super().move_handler(state, msg)
        if state != 0 and state !=4 and state !=3:
            self.bot_move()
        return _s 

    def import_board(self, fen_notation, player_and_turn_desired):
        self.stockfish.import_fen(fen_notation)
        return super().import_board(fen_notation, player_and_turn_desired)

    def mul_pieces(self, quant):
        if self.players['list'][self.turn] == self.player_bot:
            for x in range(len(quant)):
                if self.response['position'] == quant[x].position:
                    return quant[x]
        else:
            return super().mul_pieces(quant)


    def telegram_promotion(game):
        if game.players['list'][game.turn] == game.player_bot:
            selection = game.response['selection']
            game.response['selection'] = None
            return selection
        else:
            return super().telegram_promotion(game)

class Game_Database_Chess(Game_P_Chess):
    @insert_game
    def startgame(self):
        return super().startgame()

    @update_game_decorator
    def move(self, player, move):
        return super().move(player, move)
    
    @update_game_decorator
    def resign(self, resigner):
        return super().resign(resigner)
