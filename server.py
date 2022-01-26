import os
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response

# Create app
tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)


#
# The following is a dummy URI that does not connect to a valid database. You will need to modify it to connect to your Part 2 database in order to use the data.
#
# XXX: The URI should be in the format of:
#
#     postgresql://USER:PASSWORD@104.196.152.219/proj1part2
#
# For example, if you had username biliris and password foobar, then the following line would be:
#
#     DATABASEURI = "postgresql://biliris:foobar@104.196.152.219/proj1part2"
#
DATABASEURI = "postgresql://zs2531:1111@35.196.73.133/proj1part2"

#
# This line creates a database engine that knows how to connect to the URI above.
#
engine = create_engine(DATABASEURI)




@app.before_request
def before_request():
  """
  This function is run at the beginning of every web request
  (every time you enter an address in the web browser).
  We use it to setup a database connection that can be used throughout the request.

  The variable g is globally accessible.
  """
  try:
    g.conn = engine.connect()
  except:
    print("uh oh, problem connecting to database")
    import traceback; traceback.print_exc()
    g.conn = None


@app.teardown_request
def teardown_request(exception):
  """
  At the end of the web request, this makes sure to close the database connection.
  If you don't, the database could run out of memory!
  """
  try:
    g.conn.close()
  except Exception as e:
    pass


#
# @app.route is a decorator around index() that means:
#   run index() whenever the user tries to access the "/" path using a GET request
#
# If you wanted the user to go to, for example, localhost:8111/foobar/ with POST or GET then you could use:
#
#       @app.route("/foobar/", methods=["POST", "GET"])
#
# PROTIP: (the trailing / in the path is important)
#
# see for routing: http://flask.pocoo.org/docs/0.10/quickstart/#routing
# see for decorators: http://simeonfranklin.com/blog/2012/jul/1/python-decorators-in-12-steps/
#



@app.route('/',methods=['GET','POST'])
def index():
  cursor = g.conn.execute("SELECT * FROM clubs;")
  result = cursor.fetchall()
  results = [{'club_name': result[i][0],'establish_year':result[i][2],'average_market_value':result[i][1]} for i in range(20)]
  return render_template('main.html',clubs=results)


@app.route('/search1', methods=['GET','POST'])

def searchplayer():
    if request.method=="GET":
      return render_template("search1.html")
    else:
      player_name=request.form.get("player_name")
      cursor1 = g.conn.execute("SELECT * FROM players WHERE player_name='{0}'".format(player_name))
      cursor2 = g.conn.execute("SELECT * FROM club_player WHERE player_name='{0}'".format(player_name))
      result1=cursor1.fetchone()
      result2=cursor2.fetchone()
      data1=[{'player_name': result1[0],'age':result1[1],'value':result1[2],'position':result1[3],'club':result2[0]}]
      return render_template('search1.html',data1=data1)


@app.route('/search2', methods=['GET','POST'])

def searchaward():
    if request.method=="GET":
      return render_template("search2.html")
    else:
      award_id=request.form.get("award_id")
      cursor1 = g.conn.execute("SELECT * FROM awards WHERE award_id='{0}'".format(award_id))
      cursor2 = g.conn.execute("SELECT * FROM club_award WHERE award_id='{0}'".format(award_id))
      result1=cursor1.fetchone()
      result2=cursor2.fetchone()
      data2=[{'award_name':result1[1],'club':result2[0]}]
      return render_template('search2.html',data2=data2)


@app.route('/search3', methods=['GET','POST'])

def searchcoach():
    if request.method=="GET":
      return render_template("search3.html")
    else:
      coach_name=request.form.get("coach_name")
      cursor1 = g.conn.execute("SELECT * FROM coaches WHERE coach_name='{0}'".format(coach_name))
      cursor2 = g.conn.execute("SELECT * FROM club_coach WHERE coach_name='{0}'".format(coach_name))
      result1=cursor1.fetchone()
      result2=cursor2.fetchone()
      data3=[{'coach_name': result1[0],'age':result1[1],'country':result1[2],'club':result2[0]}]
      return render_template('search3.html',data3=data3)


if __name__ == "__main__":

  import click
  @click.command()
  @click.option('--debug', is_flag=True)
  @click.option('--threaded', is_flag=True)
  @click.argument('HOST', default='0.0.0.0')
  @click.argument('PORT', default=8111, type=int)
  def run(debug, threaded, host, port):

    """
    This function handles command line parameters.
    Run the server using:

        python server.py

    Show the help text using:

        python server.py --help

    """

    HOST, PORT = host, port
    print ("running on %s:%d" % (HOST, PORT))
    app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)
  run()
