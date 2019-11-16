import sqlite3
import os

class SqlAccess():
    def __init__(self,
                 name = 'reddit_data'):
        self.conn = None
        self.db_name = name
    
    def erase_data_from_db(self):
        os.remove(('{0}.db').format(self.db_name))
        self.create_or_connect_db()
    
    def create_or_connect_db(self):
        self.conn = sqlite3.connect(('{0}.db').format(self.db_name))
    
    def create():
        pass
    
    def read():
        pass
    
    def update():
        pass
    
    def delete():
        pass