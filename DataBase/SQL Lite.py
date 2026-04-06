# i see how work sqlite3, This file not need for work programm
import sqlite3
from sqlalchemy import create_engine

db = sqlite3.connect('my_database.db')

curs = db.cursor()

# curs.execute('''CREATE TABLE users (
#     name text,
#     sure_name text,
#     age integer
# )''')

# curs.execute("INSERT INTO users VALUES ('Alex', 'Sokolov', 20)")

curs.execute("SELECT rowid, * FROM users ORDER BY rowid DESC")
# print(curs.fetchall())# все данные
# print(curs.fetchmany(1))# только первые n записей
# print(curs.fetchone())# выбирает 1го пользователя
items = curs.fetchall()

# for i in items:
    # print(f'Имя {i.name}')

db.commit()

db.close()