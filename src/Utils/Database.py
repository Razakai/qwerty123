import sqlite3
from fastapi import HTTPException
from typing import Optional, Any
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
        cursor.execute("create table sensor (id varchar2(255) PRIMARY key, country varchar2(255), city varchar2(255))")
        cursor.execute("create table metrics (id integer PRIMARY KEY AUTOINCREMENT, sensor_id varchar2(255) not null, temperature float not null, humidity float not null, timestamp int not null, FOREIGN KEY (sensor_id) REFERENCES sensor(id))")
        self.db.commit()

    def executeDB(self, query, isMany, values):
        cursor = self.db.cursor()
        try:
            if isMany:
                return cursor.executemany(query, values) if values is not None else cursor.executemany(query)

            return cursor.execute(query, values) if values is not None else cursor.execute(query)

        except Exception as e:
            print('error', e)
            raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail="Database Error")

        finally:
            cursor.close()

    def fetchDB(self, query, isOne, values):
        cursor = self.db.cursor()

        try:
            if isOne:
                return cursor.execute(query, values).fetchone() if values is not None else cursor.execute(query).fetchone()

            return cursor.execute(query, values).fetchall() if values is not None else cursor.execute(query).fetchall()

        except Exception as e:
            print('error', e)
            raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail="Database Error")
        
        finally:
            cursor.close()

database = Database()

def connectDatabase():
    database.connectDB()
    database.createTables()

def disconnectDatabase():
    database.disconnectDB()

def execute(query: str, isMany: bool, values: Optional[Any]=None) -> None:
    return database.executeDB(query, isMany, values)

def fetch(query: str, isOne: bool, values: Optional[Any]=None) -> list:
    return database.fetchDB(query, isOne, values)