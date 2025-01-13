import psycopg2
import json
from config import host, user, password, db_name, port

connection = psycopg2.connect(host=host,user=user,password=password,database=db_name,port=port)
connection.autocommit = True
cursor = connection.cursor()

# TODO доделать

# В разделе Работа с ORM есть краткое повторение