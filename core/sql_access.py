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
    
    def create_or_connect_db(self, erase_first=False):
        if(erase_first):
            self.erase_data_from_db()
        
        # Creates and/or connects to SQLite database
        self.conn = sqlite3.connect(('{0}.db').format(self.db_name))
        c = self.conn.cursor()
        
        c.execute('''CREATE TABLE IF NOT EXISTS post
                     (
                     id             int         PRIMARY KEY,
                     url_id         varchar     NOT NULL,
                     url_title      varchar     NOT NULL,
                     author         varchar     NOT NULL,
                     upvote_ratio   uint8       NOT NULL,
                     score          int         NOT NULL,
                     time_created   datetime    NOT NULL,
                     num_gold       int,
                     category       varchar,
                     text           varchar,
                     main_link      varchar,
                     flairs         int,
                     comments       int
                     )
                     ''')
        
        c.execute('''CREATE TABLE IF NOT EXISTS comment
                     (
                     post_id        int         PRIMARY KEY,
                     comment_id     varchar     NOT NULL,
                     depth          int         NOT NULL,
                     next           varchar,
                     previous       varchar
                     )
                     ''')
                     
        c.execute('''CREATE TABLE IF NOT EXISTS link
                     (
                     post_id        int         PRIMARY KEY,
                     link           varchar     NOT NULL
                     )
                     ''')
        
    def save_changes(self):
        self.conn.commit()
        self.conn.close()
    
    def create(self):
        pass
    
    def read(self):
        pass
    
    def update(self):
        pass
    
    def delete(self):
        pass