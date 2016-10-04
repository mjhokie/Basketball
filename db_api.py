import sqlite3 as lite
import pandas
import json



con = lite.connect('db/Basketball.db')
sql="SELECT Player, count(case Result when 'Winner' then 1 else null end) as Wins, count(case Result when 'Loser' then 1 else null end) as Losses, count(*) as Games, round(count(case Result when 'Winner' then 1 else null end)*1.00/count(*)*1.00, 5) as Pct FROM Stats WHERE Date between '4/1/2016' and '7/12/2016' group by 1 having count(*)> 75 order by 5 desc"
c = con.cursor()

c.execute('Update Stats Set Player=Upper(Player)')

#@app.route('/api/stats', methods=['POST'])
#def pct_req():

df=pandas.read_sql(sql,con)
pct_list=df.to_dict('records')

for record in pct_list:
    for key in record:

        if key == 'Player':
          record[key]=str(record[key])

con.close()

print json.dumps(pct_list)
#return json.dumps(pct_list)