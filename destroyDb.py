import sqlite3
def dbConnection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn
with dbConnection() as connection:
    connection.execute('DROP TABLE IF EXISTS scores')