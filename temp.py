import sqlite3

conn = sqlite3.connect("data.db")
cu = conn.cursor()

cu.execute("SELECT price FROM menu WHERE item = 'burger';")
res = cu.fetchone()[0]
print(res)


# d = cu.fetchall()
# print(d)