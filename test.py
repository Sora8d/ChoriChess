from chess_bot_beta import Chess_Bot_Handler as CBHS
from chess_bot_beta import Game_Bot_Chess as GBC
import random

CBH= CBHS()
#Changes:
#Changed room['Private'] for room['Type']
def printwt(id, action):
    print(id,' : ', action)

players= {}
def chess_test_s():
    select= 'multiplayer'
    players['Jhon']= random.randint(1000,9000)
    players['Jhessica']= random.randint(1000,9000)
    res = CBH.multiplayer_t(user={'first_name': 'Jhon', 'id':players['Jhon']}, ef_id=players['Jhon'], type_chat='private')
    room= CBH.room_members[CBH.members[players['Jhon']][players['Jhon']][1]]
    game= room['Board']
#So this is so the game doesnt do anything stupid when playing in multiplayer.
    if select=='multiplayer':
        if room['Type']=='private':
            printwt(room['Players'][0][1], res)
        else:
            print(res)
    else:
        if room['Type'] != 'private':
            print(res)
        else:
            
if __name__=='__main__':
    chess_test_s()
