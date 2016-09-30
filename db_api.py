import sqlite3 as lite
import pandas
import numpy

numpy.version.version

con = lite.connect('db/Basketball.db')
sql="SELECT Player, count(case Result when 'Winner' then 1 else null end) as Wins, count(case Result when 'Loser' then 1 else null end) as Losses, count(*) as Games, round(count(case Result when 'Winner' then 1 else null end)*1.00/count(*)*1.00, 5) as Pct FROM Stats WHERE Date between '4/1/2016' and '7/12/2016' group by 1 having count(*)> 75 order by 5 desc"
#sql="SELECT  * FROM Stats "

with con:
    cur = con.cursor()
    cur.execute(" UPDATE Stats SET player =REPLACE(REPLACE(player, x'0D0A', x'0A'), x'0D', x'0A');")
    cur.execute(" UPDATE Stats SET player =REPLACE(player, '\n', '');")
#    cur.execute(sql)
#   rows = cur.fetchall()

df=pandas.read_sql(sql,con)
data=df.to_dict('records')
print data

#for row in rows:
 #       print row


