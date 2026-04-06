from DataBase.configuration import *
import pymysql

try:
    con = pymysql.connect(
        host=HOST,  # Localhost for local connection
        user=USER,
        passwd=PASSWORD,
        database=DATABASE,
        port=PORT,
        cursorclass=pymysql.cursors.DictCursor
    )
    print(con)
    print('connect is true')
except:
    print('connection fail')

def Select_all(table='users'):
    with con.cursor() as cursor:
        cursor.execute(f"SELECT * FROM {table}")
        result = cursor.fetchall()
        for row in result:
            print(row)

def Isert_record():
    with con.cursor() as cursor:
        command = "INSERT INTO book (book_title, publication_date, in_stock) VALUES (%s, %s, %s)"
        data = [
            # ['Гарри Поттер и масштабируемые сети CISO', '1997-12-1', 4],
            # ['Атлант расправил плечи', '2003-10-10', 7],
            # ['Собор без крестов', '2001-12-7', 5],
            # ['Евгений Онегин', '2007-11-04', 1],
            # ['451 по фаррингейту', '2000-12-09', 8],
            # ['Война и мир', '2001-10-12', 0],
            ['Невероятные приключения Джо Джо, гонка стального шара (1-4 том)', '2018-08-06', 0]
        ]
        # cursor.execute(command, data[0])
        for data in data:
            cursor.execute(command, (data[0], data[1], data[2]))
            con.commit()

def Delete_record():
    with con.cursor() as  cursor:
        command = "DELETE FROM book WHERE id_book > 0"
        cursor.execute(command)
        con.commit()

def Update_record():
    with con.cursor() as cursor:
        command = "UPDATE users SET name = %s WHERE id_users = %s"
        cursor.execute(command, ("Иван", 2))
        con.commit()

# Delete_record()
# Isert_record()
# Update_record()
Select_all('book')

con.close()