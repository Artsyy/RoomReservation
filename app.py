from flask import Flask, render_template, request
import sqlite3 as sql
from sqlite3 import Error
app = Flask(__name__)

reserve_id = 0
database = "classroomManager.db"

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/reserve')
def reserve():
   return render_template('reserve.html')

@app.route('/dReserve')
def dReserve():
   return render_template('dReserve.html')

# def initialize_variables():
#    global reserve_id
#    try: 
#       conn = sql.connect(database)
#       cur = conn.cursor()
#       cur.execute("""SELECT MAX(id) FROM reservation""")
#       row = cur.fetchone()
#       reserve_id = row[0] 
#    except Error as e:
#       print(e)

def validate(building, room, date, t1, t2):
   try: 
      conn = sql.connect(database)
      cur = conn.cursor()
      
      cur.execute("""SELECT COUNT(*) FROM reservation
          WHERE building LIKE ? AND room_number = ? 
          AND date = ? AND start_time >= ? AND end_time <= ?;""", 
         (building, room, date, t1, t2))
      row1 = cur.fetchone()

      cur.execute("""SELECT count(*) FROM room 
      WHERE building LIKE ? AND room_number LIKE ?;""", (building, room))
      row2 = cur.fetchone()
      print(row1, row2)
      if row1[0] == 0 and row2[0] != 0:
         return True
      else:
         return False
   except Error as e:
      print(e)

def getUser(name, email):
   try:
      conn = sql.connect(database)
      cur = conn.cursor()
      cur.execute("SELECT id FROM users WHERE email LIKE ? AND name LIKE ?", (email, name))
      row = cur.fetchone()
      return row[0]
   except Error as e:
      print(e)


@app.route('/deleteReserve', methods = ['POST', 'GET'])
def deleteReserve():
   print("Deleteing Reserve")
   date = request.form['Date']
   start = request.form['Start']
   end = request.form['End']
   host = getUser(request.form['Host'], request.form['Email'])
   print(date, start, end, host)
   try:
      conn = sql.connect(database)
      cur = conn.cursor()
      cur.execute("""DELETE FROM reservation WHERE date = ? 
         AND start_time = ? AND end_time = ? AND organizer_id = ?""", 
         (date, start, end, host) )
      row = cur.fetchone()
      return row[0]
   except Error as e:
      print(e)

@app.route('/makeReserve', methods = ['POST', 'GET'])
def makeReserve():
   global reserve_id
   building = request.form['Building']
   room = request.form['Room']
   title = request.form['Event']
   date = request.form['Date']
   start = request.form['Start']
   end = request.form['End']
   comment = request.form['Comment']
   host = getUser(request.form['Host'], request.form['Email'])
   print(reserve_id, building, room, title, date, start, end, comment, host)
   if request.method == 'POST' and validate(building, room, date, start, end):
      try:
         
         with sql.connect(database) as con:
            cur = con.cursor()
            
            # Accept invitation only from qualified users && no conflict
            cur.execute("""INSERT INTO reservation(id, building, room_number, title, date, start_time, end_time, description, organizer_id) 
               VALUES (?,?,?,?,?,?,?,?,?)""", (reserve_id, building, room, title, date, start, end, comment, host) )

            con.commit()
            msg = "Reservation successful"
            reserve_id += 1
      except:
         con.rollback()
         msg = "Error in Reserve Operation"
         print(reserve_id, building, room, title, date, start, end, comment, host)
   # Message corresponding to success/error in insert operation rendered
      finally:
         return render_template("result.html",msg = msg)
         con.close()
   else:
      msg = "Request invalid, conflict with existing reservation. Or the desired location does not exist"
      return render_template("result.html",msg = msg)


def main():
   # global reserve_id
   # initialize_variables
   app.run(debug = True)


if __name__ == '__main__':
   main()
   # app.run(debug = True)