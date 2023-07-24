import logging
import sqlite3
from Log_Config import *
from datetime import datetime


def all_Tasks():
    Base = sqlite3.connect("DataBase.sqllite")

    cursor = Base.cursor()

    cursor.execute("SELECT * FROM ToDo")
    result = cursor.fetchall()

    cursor.close()
    Base.close()
    return result


def all_Tasks_Write_Down(Task, Data, Time):
    try:
        Base = sqlite3.connect("DataBase.sqllite")

        cursor = Base.cursor()
        cursor.execute("INSERT INTO ToDo (Task, Data, Time) VALUES (?, ?, ?)", (Task, Data, Time))
        Base.commit()

        cursor.close()
        Base.close()
        logging.info('Новая задача добавлена')

        return True

    except BaseExceptionGroup as BEG:
        logging.error(BEG)
        return False


def Delete_Task(task, date, time):
    Base = sqlite3.connect("DataBase.sqllite")

    cursor = Base.cursor()

    cursor.execute("DELETE FROM ToDo WHERE Task=? AND Data=? AND Time=?", (task, date, time))
    Base.commit()

    cursor.close()
    Base.close()

def Get_Data(data):
    Base = sqlite3.connect("DataBase.sqllite")

    cursor = Base.cursor()

    cursor.execute("SELECT Task, Time, Data FROM ToDo WHERE Data=? ", (data,))
    result = cursor.fetchall()

    cursor.close()
    Base.close()
    return result
