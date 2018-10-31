import sqlite3


connection = sqlite3.connect('data.db')
cursor = connection.cursor()

create_table = "CREATE TABLE IF NOT EXISTS pages (id INTEGER PRIMARY KEY, url text)"
cursor.execute(create_table)



cursor.execute("INSERT INTO pages VALUES (1, 'http://new.abb.com/future')")

connection.commit()
connection.close()