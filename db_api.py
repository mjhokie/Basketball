import sqlite3 as lite
import pandas
import json
import csv

from datetime import datetime

con = lite.connect('db/Basketball.db')


conb = lite.connect(":memory:")

#sql="SELECT Player, count(case Result when 'Winner' then 1 else null end) as Wins, count(case Result when 'Loser' then 1 else null end) as Losses, count(*) as Games, round(count(case Result when 'Winner' then 1 else null end)*1.00/count(*)*1.00, 5) as Pct FROM Stats WHERE Date between '2014-09-15' and '2014-09-20' group by 1 having count(*)> 1 order by 5 desc"
cur = con.cursor()
#@app.route('/api/stats', methods=['POST']
#def pct_req():

file="/Users/JamieJackson/Documents/Development/Basketball/test2.csv"

df2=pandas.read_csv(file)

#pct_list=df.to_dict('records')

cur.execute("Drop TABLE Stats")
cur.execute("CREATE TABLE Stats (Date, Player, Game, Result);") # use your column names here

with open('/Users/JamieJackson/Documents/Development/Basketball/test2.csv','rU') as fin: # `with` statement available in 2.5+
    # csv.DictReader uses first line in file for column headings by default
    dr = csv.DictReader(fin) # comma is default delimiter
    to_db = [(i['Date'], i['Player'], i['Game'], i['Result']) for i in dr]

cur.executemany("INSERT INTO Stats (Date, Player, Game, Result) VALUES (?, ?, ?, ?);", to_db)
con.commit()
conb.close()

cur.execute('Update Stats Set Player=Upper(Player)')
sql="select * from Stats "


df=pandas.read_sql(sql,con)

#for record in pct_list:
 #   for key in record:

  #      if key == 'Player':
   #       record[key]=str(record[key])

con.close()

print df
#print json.dumps(pct_list)
#return json.dumps(pct_list)