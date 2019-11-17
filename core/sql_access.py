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
                     id             INTEGER     PRIMARY KEY     AUTOINCREMENT,
                     url            varchar     NOT NULL,
                     url_id         varchar     NOT NULL,
                     url_title      varchar     NOT NULL,
                     author         varchar     NOT NULL,
                     upvote_ratio   uint8       NOT NULL,
                     score          int         NOT NULL,
                     time_created   datetime    NOT NULL,
                     num_gold       int,
                     num_comments   int,
                     category       varchar,
                     text           varchar,
                     main_link      varchar,
                     flairs         int,
                     comments       int
                     )
                     ''')
        
        c.execute('''CREATE TABLE IF NOT EXISTS comment
                     (
                     post_id        INTEGER     PRIMARY KEY     AUTOINCREMENT,
                     comment_id     varchar     NOT NULL,
                     depth          int         NOT NULL,
                     next           varchar,
                     previous       varchar
                     )
                     ''')
                     
        c.execute('''CREATE TABLE IF NOT EXISTS link
                     (
                     post_id        INTEGER     PRIMARY KEY     AUTOINCREMENT,
                     link           varchar     NOT NULL
                     )
                     ''')
        
    def save_changes(self):
        self.conn.commit()
        self.conn.close()
        
    def _question_mark_creator(self,
                               n_question_marks):
        final_string = ''
        
        for i in range(n_question_marks):
            final_string += '?,'
            
        final_string += '?'
        
        return final_string

    def insert(self,
               table,
               data):
        c = self.conn
        
        cols = c.execute(('''
                        PRAGMA table_info({0})
                        ''').format(table))
        num_cols = sum([1 for i in cols]) - 1
        question_marks = self._question_mark_creator(num_cols)
        
        if table == 'post':
            c.execute(('''INSERT INTO {0}
                          VALUES ({1})'''
                      ).format(table, question_marks), data)
    