from core.sql_access import SqlAccess
import pandas as pd

SQL = SqlAccess()
SQL.create_or_connect_db()
c = SQL.conn

df = pd.read_sql_query("SELECT * FROM post", c)

df.to_csv('data/r-machinelearning.csv', columns=df.columns, index=False)