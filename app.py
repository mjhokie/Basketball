
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, _app_ctx_stack
from sqlite3 import dbapi2 as sqlite3
import pandas
import json


# configuration
DATABASE = 'db/Basketball.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'


# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)


def init_db():
    """Creates the database tables."""
    with app.app_context():
        db = get_db()
        db.commit()


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    top = _app_ctx_stack.top
    if not hasattr(top, 'db/Basketball.db'):
        sqlite_db = sqlite3.connect(app.config['DATABASE'])
        sqlite_db.row_factory = sqlite3.Row
        top.sqlite_db = sqlite_db

    return top.sqlite_db

@app.teardown_appcontext
def close_db_connection(exception):
    """Closes the database again at the end of the request."""
    top = _app_ctx_stack.top
    if hasattr(top, 'db/Basketball.db'):
        top.sqlite_db.close()



#sql="SELECT Player, count(case Result when 'Winner' then 1 else null end) as Wins, count(case Result when 'Loser' then 1 else null end) as Losses, count(*) as Games, round(count(case Result when 'Winner' then 1 else null end)*1.00/count(*)*1.00, 5) as Pct FROM Stats WHERE Date between '4/1/2016' and '7/12/2016' group by 1 having count(*)> 75 order by 5 desc"

@app.route('/')
def show_entries():
    db = get_db()
    cur = db.execute('SELECT UPPER(Player) as Player, count(case Result when "Winner" then 1 else null end) as Wins, count(case Result when "Loser" then 1 else null end) as Losses, count(*) as Games, round(count(case Result when "Winner" then 1 else null end)*1.00/count(*)*1.00, 5) as Pct FROM Stats WHERE Date >= "4/1/2016" group by 1 having count(*)> 100 order by 5 desc')
    entries = cur.fetchall()
    return render_template('index.html', entries=entries)

@app.route('/showHome') 
def showHome(): 
    return render_template('index.html')
    
@app.route('/api/showstats', methods=['GET', 'POST'])
def showstats():
   # get_data=json.loads(request.data)
    #print get_data

    #games=str(get_data['games'])
   return render_template('stats.html')



@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('index'))


if __name__ == '__main__':
    init_db()
    app.run()

