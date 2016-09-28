import sqlite3 as lite




con = lite.connect('db/Basketball.db')
sql="SELECT * FROM Stats WHERE Date between '4/1/2016' and '7/12/2016' and player='mj' order by 1,2"

with con:
    cur = con.cursor()
    cur.execute(" UPDATE Stats SET player =REPLACE(REPLACE(player, x'0D0A', x'0A'), x'0D', x'0A');")
    cur.execute(" UPDATE Stats SET player =REPLACE(player, '\n', '');")
    cur.execute(sql)
    rows = cur.fetchall()

for row in rows:
        print row


