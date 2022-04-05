import sqlite3


class Processor:

    def find_user(self, name):
        connection = sqlite3.connect('users.db')
        cur = connection.cursor()
        result = None
        for row in cur.execute("select id, name from users where name = :name", {"name": name}):
            result = row[1]
        connection.close()
        return result

    def __init__(self):
        con = sqlite3.connect('users.db')
        cur = con.cursor()
        cur.execute("create table IF NOT EXISTS users (id int, name text, pass_hash text)")
        cur.execute("insert into users values (1,'Tom', '12')")
        con.commit()
        con.close()
