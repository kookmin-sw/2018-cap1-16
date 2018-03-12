from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from pymongo.errors import OperationFailure
import os, time, re, getpass

def connect_db(ip,port):
	client = MongoClient('mongodb://%s:%d' %(ip,port), serverSelectionTimeoutMS = 1500)
	
	return client

def check_connection():
	try : 
		client.admin.command('ismaster')
	except ConnectionFailure:
		print("Server is not available")
		exit()
	

def get_db(client,db_name):
	while(True):
		user_id , user_pwd = get_authenticate()
		db = client[db_name]
		try:
			db.authenticate(user_id,user_pwd)
		except OperationFailure:
			print("Failed to login")
			continue

		print('Login successfully')
		break

	return db

def get_authenticate():
	user_id = ' '
	input_id_first = True
	while not re.match("^[A-Za-z0-9]+$", user_id):
		if not input_id_first:
			print("Error! you can use only Alphabet or Number for your id")
		user_id = input("ID: ")
		input_id_first = False
			
	user_pwd = getpass.getpass()

	return user_id, user_pwd

def get_collection(db,collection_name):
	collection = db[collection_name]

	return collection

if __name__ == '__main__':
	client = connect_db('localhost',27017)
	check_connection()
	db = get_db(client,'seclab')
	collection = get_collection(db,'analyzed_report')