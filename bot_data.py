import sqlite3

#create a class that allows me to connect to a mySQL database as well as functions to perform CRUD operations on it within the class
class Database:
    def __init__(self, database_name):
        self.database_name = database_name

    def connect(self):
        try:
            self.connection =  sqlite3.connect(self.database_name) # db will be created or opened
            self.cursor = self.connection.cursor()
            print("Successfully connected to database")
        except:
            print("Failed to connect to database")

    def disconnect(self):
        try:
            self.connection.close()
            print("Successfully disconnected from database")
        except:
            print("Failed to disconnect from database")

    def create_table(self, table_name, columns):
        try:
            query = f"CREATE TABLE {table_name} ({columns})"
            self.cursor.execute(query)
            self.connection.commit()
            print(f"Successfully created table {table_name}")
        except:
            print(f"Failed to create table {table_name}")

    def insert(self, table_name, columns, values):
        try:
            query = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"
            self.cursor.execute(query)
            self.connection.commit()
            print(f"Successfully inserted {values} into {table_name}")
            return self.cursor.lastrowid
        except:
            print(f"Failed to insert {values} into {table_name}")
            return None

    def select(self, table_name, columns, condition):
        try:
            query = f"SELECT {columns} FROM {table_name} WHERE {condition}"
            self.cursor.execute(query)
            self.connection.commit()
            print(f"Successfully selected {columns} from {table_name} where {condition}")
            return self.cursor.fetchall()
        except:
            print(f"Failed to select {columns} from {table_name} where {condition}")

    def update(self, table_name, set, condition):
        try:
            query = f"UPDATE {table_name} SET {set} WHERE {condition}"
            self.cursor.execute(query)
            self.connection.commit()
            print(f"Successfully updated {table_name} set {set} where {condition}")
        except:
            print(f"Failed to update {table_name} set {set} where {condition}")

    def delete(self, table_name, condition):
        try:
            query = f"DELETE FROM {table_name} WHER4E {condition}"
            self.cursor.execute(query)
            self.connection.commit()
            print(f"Successfully deleted from {table_name} where {condition}")
        except:
            print(f"Failed to delete from {table_name} where {condition}")

    def execute(self, query):
        try:
            self.cursor.execute(query)
            self.connection.commit()
            print(f"Successfully executed {query}")
        except:
            print(f"Failed to execute {query}")

