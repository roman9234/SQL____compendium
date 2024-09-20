import psycopg2
import json
from config import host, user, password, db_name, port

connection = psycopg2.connect(host=host,user=user,password=password,database=db_name,port=port)
connection.autocommit = True
cursor = connection.cursor()

# TODO вынести подключение в отдельный класс

cursor.execute("SELECT * FROM sys.databases d")
res = cursor.fetchall()
print(res)