import sqlite3
from datetime import datetime


def all_Tasks():
    Base = sqlite3.connect("DataBase.sqllite")
    cursor = Base.cursor()
    cursor.execute("SELECT * FROM ToDo")
    result = cursor.fetchall()
    cursor.close()
    Base.close()
    return result