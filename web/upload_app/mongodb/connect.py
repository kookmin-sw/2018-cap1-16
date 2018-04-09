from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from pymongo.errors import OperationFailure
import re, getpass


class SeclabMongoClient:
    def __init__(self, ip, port, db):
        self.client = self.connect_db(ip, port)
        self.check_connection()
        self.db = self.get_db(db, 0)

    # self.collection = self.get_collection(collection)

    def connect_db(self, ip, port):
        client = MongoClient('mongodb://%s:%d' % (ip, port), serverSelectionTimeoutMS=1500)

        return client

    def check_connection(self):
        try:
            self.client.admin.command('ismaster')
        except ConnectionFailure:
            print("Server is not available")
            exit()

    def get_db(self, db_name, auth):
        db = self.client[db_name]

        if auth == 1:
            while (True):
                user_id, user_pwd = self.get_authenticate()
                try:
                    db.authenticate(user_id, user_pwd)
                except OperationFailure:
                    print("Failed to login")
                    continue

                print('Login successfully')
                break

        return db

    def get_authenticate(self):
        user_id = ' '
        input_id_first = True
        while not re.match("^[A-Za-z0-9]+$", user_id):
            if not input_id_first:
                print("Error! you can use only Alphabet or Number for your id")
            user_id = input("ID: ")
            input_id_first = False

        user_pwd = getpass.getpass()

        return user_id, user_pwd

    def get_collection(self, collection_name):
        collection = self.db[collection_name]

        return collection