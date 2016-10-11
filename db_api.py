import sqlite3 as lite
import pandas as pd
import csv
import os

from datetime import datetime

pd.set_option('display.max_rows',1000)
pd.set_option('display.max_columns',5000)
pd.set_option('display.width',5000)

con = lite.connect('db/Basketball.db')


conb = lite.connect(":memory:")

cur = con.cursor()


base_path = r"/Users/JamieJackson/Documents/Development/Basketball"
file_path = os.path.join(base_path,'Official Lunch Ball Stats_09_19_16.xlsm')
winners = pd.read_excel(file_path,'Data',index_col = 0, usecols=[0,1,2])


win2 = pd.read_excel(file_path,'Data',index_col = 0, usecols=[0,1,3])
win2['Player 1 ']=win2['Player 2']
del win2['Player 2']
winners=winners.append(win2, ignore_index=False)

win3 = pd.read_excel(file_path,'Data',index_col = 0, usecols=[0,1,4])
win3['Player 1 ']=win3['Player 3']
del win3['Player 3']
winners=winners.append(win3, ignore_index=False)

win4 = pd.read_excel(file_path,'Data',index_col = 0, usecols=[0,1,5])
win4['Player 1 ']=win4['Player 4']
del win4['Player 4']
winners=winners.append(win4, ignore_index=False)

win5 = pd.read_excel(file_path,'Data',index_col = 0, usecols=[0,1,6])
win5['Player 1 ']=win5['Player 5']
del win5['Player 5']
winners=winners.append(win5, ignore_index=False)



winners['Result']="Winner"
#winners['Player']=map(lambda x: x.upper(), winners['Player 1 '])
winners['Player']=winners['Player 1 ']


losers = pd.read_excel(file_path,'Data',index_col = 0, usecols=[0,1,7])

loss2 = pd.read_excel(file_path,'Data',index_col = 0, usecols=[0,1,8])
loss2['P1']=loss2['P2']
del loss2['P2']
losers=losers.append(loss2, ignore_index=False)

loss3 = pd.read_excel(file_path,'Data',index_col = 0, usecols=[0,1,9])
loss3['P1']=loss3['P3']
del loss3['P3']
losers=losers.append(loss3, ignore_index=False)


loss4 = pd.read_excel(file_path,'Data',index_col = 0, usecols=[0,1,10])
loss4['P1']=loss4['P4']
del loss4['P4']
losers=losers.append(loss4, ignore_index=False)

loss5 = pd.read_excel(file_path,'Data',index_col = 0, usecols=[0,1,11])
loss5['P1']=loss5['P5']
del loss5['P5']
losers=losers.append(loss5, ignore_index=False)



losers['Result']="Loser"
#losers['Player']=map(lambda x: x.upper(), losers['P1'])
losers['Player']=losers['P1']



Stats=winners.append(losers, ignore_index=False)


del Stats['P1']
del Stats['Player 1 ']
Stats['Game']=Stats['Game #']
del Stats['Game #']

Stats = Stats.reindex(columns=['Game', 'Player', 'Result'])

Stats.to_csv('test2.csv')

file="/Users/JamieJackson/Documents/Development/Basketball/test2.csv"

df2=pd.read_csv(file)

#print df2

cur.execute("Drop TABLE Stats")
cur.execute("CREATE TABLE Stats (Date, Player, Game, Result);") # use your column names here

with open('/Users/JamieJackson/Documents/Development/Basketball/test2.csv','rU') as fin: # `with` statement available in 2.5+
    # csv.DictReader uses first line in file for column headings by default
    dr = csv.DictReader(fin) # comma is default delimiter
    to_db = [(i['Date'], i['Player'], i['Game'], i['Result']) for i in dr]

cur.executemany("INSERT INTO Stats (Date, Player, Game, Result) VALUES (?, ?, ?, ?);", to_db)
con.commit()
conb.close()

#cur.execute('Update Stats Set Player=Upper(Player)')
sql="select * from Stats "


df=pd.read_sql(sql,con)


con.close()
#print df
