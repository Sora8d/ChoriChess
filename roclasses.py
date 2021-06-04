#This i created to make room handling easy, it can accept sid's and usernames
class ro_manager:
    def __init__(self):
        self.r_q= 0
        self.rooms_list= []
        self.room_members= {}
        self.members= {}
        self.C_A= {0: self.delete_room, 1: lambda x: None, 2: lambda x: None}
#This one checks if the rooms are full, beware that this checks a list in python,
#Therefore if something malfunctions, it doesnt really check the size of the room
    def check_room(self, c_name):
#Creates room
        if len(self.rooms_list) == 0:
            return self.create_room()
        else:
#If there is a room with space, in you go
            for x in self.rooms_list:
#This checks if the room is full, or if youre already on that room
                if len(self.room_members[x]) < 2 or c_name in self.room_members[x]:
                    return x
                else:
                    continue
#Creates room
        return self.create_room()
    def create_room(self):
            self.r_q+=1
            self.rooms_list.append('room{}'.format(self.r_q))
            self.room_members[self.rooms_list[-1]]= set()
            return self.rooms_list[-1]
#This one checks the users, since websockets tend to reconnect
#(sometimes without disconnecting) this thing checks if the user
#hasnt been assigned a room, and if it has, it gives the correct room
    def put_users(self, username, sid, room):
        self.members[sid] = []
        self.members[sid].append(username)
        self.members[sid].append(room)
        self.room_members[room].add(username)
        for x, i in self.room_members.items():
            print(x + ' has ' + str(i))
        print('ends here \n')
        return room
#When a user disconnects
    def pop_user(self, sid, room):
        self.room_members[room].remove(self.members[sid][0])
        self.members.pop(sid)
        self.C_A[len(self.room_members[room])](room)
        print('lefted room')

#This gets to the diccionary up in the class
    def delete_room(self, ro):
        self.room_members.pop(ro)
        self.rooms_list.remove(ro)
