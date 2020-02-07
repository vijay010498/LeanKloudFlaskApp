from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re


app = Flask(__name__)
app.secret_key = 'Lean_Kloud'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Vijay123'
app.config['MYSQL_DB'] = 'ToDoList'

mysql = MySQL(app)



@app.route('/LeanKloudApp/', methods=['GET', 'POST'])
def login(): 
    msg='WELCOME'
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM adminaccounts WHERE username = %s AND password = %s', (username, password))
        res=cursor.fetchone()
        if res:
            return render_template('admin.html')
        cursor.execute('SELECT * FROM stdaccounts WHERE username = %s AND password = %s', (username, password))
        res=cursor.fetchone()
        if res:
            return render_template('stduser.html')
        else:
            msg='Incorrect username/password!'
    return render_template('index.html',msg=msg)
    
    
    
@app.route('/add',methods=['POST'])
def add():
    content=request.form['content']
    due_by=request.form['due_date']
    cur_status='Not started'
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("insert into TODO values (NULL,%s,%s,%s)",(content,due_by,cur_status))
    mysql.connection.commit()
    msg = 'TODO ADDED'
    return render_template('admin.html',msg=msg)
   
@app.route('/search',methods=['GET', 'POST'])
def search():
    id = request.form['ID']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM TODO WHERE ID = %s", (id))
    data=cursor.fetchall()
    return render_template('admin.html',results=data)
  
@app.route('/modify',methods=['GET', 'POST'])
def modify():
    id = request.form['IDMOD']
    date = request.form['DueDateMOD']
    opt = request.form['OPTMOD']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("UPDATE TODO SET due_by=%s,status=%s WHERE ID=%s",(date,opt,id))
    mysql.connection.commit()
    msg = 'TODO UPDATED'
    return render_template('admin.html',msg=msg)

@app.route('/stdsearch',methods=['GET', 'POST'])
def stdsearch():
     opt = request.form['STDOPT']
     cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
     cursor.execute("SELECT * FROM TODO WHERE STATUS like %s", [opt])
     data=cursor.fetchall()
     return render_template('stduser.html',results=data)
     

     

if __name__== '__Main__':
    app.run(debug=True)
        