import sqlite3


def all_Tasks():
    Base=sqlite3.connect("DataBase.sqllite")
    cursor=Base.cursor()
    cursor.execute("SELECT * FROM ToDo")
    result=cursor.fetchall()
    cursor.close()
    Base.close()
    return result

print(all_Tasks()[0][0])