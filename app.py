from flask import Flask, render_template, request
import sqlite3 as sql
app = Flask(__name__)

@app.route('/')
def index():
	return "this is a test"

@app.route('/enternew')
def newRoom():
   return render_template('room.html')

@app.route('/adding',methods = ['POST', 'GET'])
def adding():
   if request.method == 'POST':
      try:
         building = request.form['building']
         room_number = request.form['room_number']
         capacity = request.form['capacity']
         description = request.form['description']
         
         with sql.connect("classroomManager.db") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO room (building,room_number,capacity,description) VALUES (?,?,?,?)",(building,room_number,capacity,description))
            
            con.commit()
            msg = "Record successfully added"
      except:
         con.rollback()
         msg = "error in insert operation"
      
      finally:
         return render_template("result.html",msg = msg)
         con.close()

@app.route('/list')
def list():
   con = sql.connect("classroomManager.db")
   con.row_factory = sql.Row
   
   cur = con.cursor()
   cur.execute("select * from room")
   
   rows = cur.fetchall(); 
   return render_template("list.html",rows = rows)

if __name__ == '__main__':
   app.run(debug = True)