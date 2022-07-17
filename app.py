from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re  

app = Flask(__name__) 

app.secret_key = 'xyzsdfg'
  
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'organisations'
  
mysql = MySQL(app)  


@app.route('/login', methods =['GET', 'POST'])
def login():
    mesage = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE email = % s AND password = % s', (email, password, ))
        user = cursor.fetchone()
        if user:            
                session['loggedin'] = True
                session['id'] = user['id']
                session['nom'] = user['nom']
                session['email'] = user['email']
                mesage = 'Logged in successfully !'
                return redirect(url_for('users'))
         
        else:
            mesage = 'Please enter correct email / password !'
    return render_template('login.html', mesage = mesage)

@app.route("/users", methods =['GET', 'POST'])
def users():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users')
        users = cursor.fetchall()    
        return render_template("users.html", users = users)
    return redirect(url_for('login'))

# @app.route("/edit", methods =['GET', 'POST'])
# def edit():
#     msg = ''    
#     if 'loggedin' in session:
#         editUserId = request.args.get('id')
#         cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#         cursor.execute('SELECT * FROM users WHERE id = % s', (editUserId, ))
#         editUser = cursor.fetchone()
#         if request.method == 'POST' and 'nom' in request.form and 'id' in request.form and 'roles' in request.form and 'prenom' in request.form :
#             nom = request.form['nom']   
#             role = request.form['roles']
#             prenom = request.form['prenom']            
#             id = request.form['id']
#             if not re.match(r'[A-Za-z0-9]+', nom):
#                 msg = 'name must contain only characters and numbers !'
#             else:
#                 cursor.execute('UPDATE users SET  nom =% s, roles =% s, prenom =% s WHERE id =% s', (nom, role, prenom, (id, ), ))
#                 mysql.connection.commit()
#                 msg = 'User updated !'
#                 return redirect(url_for('users'))
#         elif request.method == 'POST':
#             msg = 'Please fill out the form !'        
#         return render_template("edit.html", msg = msg, editUser = editUser)
#     return redirect(url_for('login'))

if __name__ == "__main__":
    app.run()