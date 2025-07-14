from tinydb import Query, TinyDB
from Database.Chat import Chat
from Database.User import User


class Database:
    def __init__(self, client, filepath):
        self.__db1, self.__db2 = filepath
        self.__userdb = TinyDB(self.__db1)
        self.__chatdb = TinyDB(self.__db2)
        self.query = Query()
        self.__client = client  
    
    @property
    def User(self):
        return User(self.__userdb, self.query, self.__client)

    @property
    def Chat(self):
        return Chat(self.__chatdb, self.query)


