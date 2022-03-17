import sqlite3
from fastapi import HTTPException
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR

class Database():
    def __init__(self):
        self.db = None
    
    def connectDB(self):
        self.db = sqlite3.connect(':memory:', check_same_thread=False)
        self.db.row_factory = sqlite3.Row
    
    def disconnectDB(self):
        self.db.close()

    def createTables(self):
        cursor = self.db.cursor()
        cursor.execute("create table sensor (id integer PRIMARY key, country varchar2(255), city varchar2(255))")
        cursor.execute("create table metrics (id integer PRIMARY KEY AUTOINCREMENT, sensor_id int not null, temperature float not null, humidity float not null, timestamp int not null, FOREIGN KEY (sensor_id) REFERENCES sensor(id))")
        self.db.commit()

    def execute(self, query, isMany, values):
        cursor = self.db.cursor()
        try:
            if isMany:
                return cursor.executemany(query, values)

            return cursor.execute(query, values)

        except Exception as e:
            print(e)
            raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail="Database Error")

        finally:
            self.db.commit()

    def fetch(self, query, isOne, values):
        cursor = self.db.cursor()

        try:
            if isOne:
                return cursor.execute(query, values).fetchone()

            return cursor.execute(query, values).fetchall()

        except Exception as e:
            raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail="Database Error")
        

database = Database()

def connectDatabase():
    database.connectDB()
    database.createTables()

def disconnectDatabase():
    database.disconnectDB()

def execute(query, isMany, values=None) -> int:
    return database.execute(query=query, isMany=isMany, values=values)

def fetch(query, isOne, values=None) -> list or dict:
    return database.fetch(query, isOne, values)