import shelve
from states import UserState


class Database(object):

    def __init__(self):
        self.__db = shelve.open("./data/UserStates")

    def UpdateUser(self, user_id, new_state):
        user_id = str(user_id)
        self.__db[user_id] = new_state
        self.__db.sync()

    def GetUserState(self, user_id):
        user_id = str(user_id)
        if user_id not in self.__db:
            self.__db[user_id] = UserState.START
        return self.__db[user_id]


class Operate(object):

    def __init__(self):
        self.__db = shelve.open("./data/UserTasks")

    def Add_Tasks(self, user_id, taska):
        user_id = str(user_id)
        if user_id not in self.__db:
            self.__db[user_id] = [[taska, 0]]
        else:
            db_list = self.__db[user_id]
            db_list.append([taska, 0])
            self.__db[user_id] = db_list
        self.__db.sync()

    def Get_Tasks(self, user_id):
        user_id = str(user_id)
        return self.__db[user_id]

    def Mark(self, user_id, index):
        user_id = str(user_id)
        db_list = self.__db[user_id]
        t = db_list[int(index)][1]
        db_list[int(index)][1] = abs(1 - t)
        self.__db[user_id] = db_list
        self.__db.sync()

    def Erase(self, user_id, index):
        user_id = str(user_id)
        db_list = self.__db[user_id]
        db_list.remove(db_list[int(index)])
        self.__db[user_id] = db_list
        self.__db.sync()


class Local_Message_Id(object):

    def __init__(self):
        self.__db = shelve.open("./data/Local_Id")

    def Change_Id_Message(self, user_id, message_id, function):
        user_id = str(user_id)
        function = str(function)
        if user_id not in self.__db:
            self.__db[user_id] = dict()
        buffer = self.__db[user_id]
        buffer[function] = message_id
        self.__db[user_id] = buffer
        print(buffer)
        self.__db.sync()

    def Get_Id_Message(self, user_id, function):
        function = str(function)
        user_id = str(user_id)
        return self.__db[user_id][function]
