import sqlite3

conn = sqlite3.connect('db.sqlite')



cursor = conn.execute("SELECT * FROM cabrillo_log_v2")
for row in cursor:
    print(row)
