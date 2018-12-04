from flask import Flask, render_template, request, url_for, redirect, flash
import sqlite3 as sql

app = Flask(__name__)
app.secret_key = "db project"

@app.route('/')
def index():
    return render_template('index.html')
 
@app.route('/search', methods = ['POST', 'GET'])
def search():
	if request.method == 'POST':
		try:
			building = request.form['building']
			room_number = request.form['room_number']
			capacity = request.form['capacity']
			room_type = request.form['room_type']

			with sql.connect("classroomManager.db") as con:
				cur = con.cursor()
				cur.execute("SELECT * FROM room WHERE building = ? OR room_number = ?", (building,room_number,))

				rows = cur.fetchall()
				#print(rows)
				print(building)
				print(room_number)

				con.commit()

				con.row_factory = sql.Row

				cur = con.cursor()
				cur.execute("SELECT * FROM room WHERE building = ? OR room_number = ?", (building,room_number,))

				rows = cur.fetchall();

				print(building)
				print(room_number)
			
				return render_template("lists.html", rows = rows)
				con.close()

		except:
			con.rollback()
			msg = "error in search operation"
			return ''

# @app.route('/enternew')
# def newRoom():
#    return render_template('room.html')

"""don't need this functionality just testing if the db can be modified but look @ this if want to add reservations"""
# @app.route('/adding', methods = ['POST', 'GET'])
# def adding():
# 	if request.method == 'POST':
# 		try:
# 			building = request.form['building']
# 			room_number = request.form['room_number']
# 			capacity = request.form['capacity']
# 			description = request.form['description']

# 			with sql.connect("classroomManager.db") as con:
# 				cur = con.cursor()
# 				cur.execute("INSERT INTO room (building,room_number,capacity,description) VALUES (?,?,?,?)",(building,room_number,capacity,description))

# 				con.commit()
# 				msg = "Record successfully added"

# 		except:
# 			con.rollback()
# 			msg = "error in insert operation"

# 		finally:
# 			return render_template("result.html", msg = msg)
# 			con.close()

"""shows the the total list of all the rooms if user doesn't want to search"""
@app.route('/list')
def list():
   con = sql.connect("classroomManager.db")
   con.row_factory = sql.Row
   
   cur = con.cursor()
   cur.execute("select * from room")
   
   rows = cur.fetchall(); 
   return render_template("list.html", rows = rows)

if __name__ == '__main__':
   app.run(debug = True)