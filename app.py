from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re  

app = Flask(__name__) 

app.secret_key = 'xyzsdfg'
  
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'organisation'
  
mysql = MySQL(app)  

#login
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

#affichage des utilisateurs
@app.route("/users", methods =['GET', 'POST'])
def users():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users')
        users = cursor.fetchall()    
        return render_template("users.html", users = users)
    return redirect(url_for('login'))

@app.route('/register', methods =['GET', 'POST'])
def register():
    mesage = ''
    if request.method == 'POST' and 'email' in request.form and'email' in request.form :
        nom = request.form['nom']
        prenom = request.form['prenom']
        password = request.form['password']
        email = request.form['email']
        date_adhesion = request.form['date_adhesion']
        tel = request.form['tel']
        avatar_photo = request.form['avatar_photo']
       
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE email = % s', (email, ))
        account = cursor.fetchone()
        if account:
            mesage = 'User already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            mesage = 'Invalid email address !'
        elif not email or not password  :
            mesage = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO users VALUES (NULL, % s, % s, % s, % s, % s, %s, %s)', (nom, prenom, password, email, date_adhesion, tel, avatar_photo))
            mysql.connection.commit()
            mesage = 'New user created!'
    elif request.method == 'POST':
        mesage = 'Please fill out the form !'
    return render_template('register.html', mesage = mesage)

@app.route("/edit", methods =['GET', 'POST'])
def edit():
    msg = ''    
    if 'loggedin' in session:
        editUserId = request.args.get('id')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE id = % s', (editUserId, ))
        editUser = cursor.fetchone()
        if request.method == 'POST' and 'nom' in request.form  and 'prenom' in request.form and 'password' in request.form and 'email' in request.form and 'date_adhesion' in request.form and 'tel' in request.form and 'avatar_photo' in request.form  :
            nom = request.form['nom']
            prenom = request.form['prenom']
            password = request.form['password']
            email = request.form['email']
            date_adhesion = request.form['date_adhesion']
            tel = request.form['tel']
            avatar_photo = request.form['avatar_photo']          
            userId = request.form['id']
            if not re.match(r'[A-Za-z0-9]+', nom):
                msg = 'name must contain only characters and numbers !'
            else:
                cursor.execute('UPDATE users SET  nom =% s,prenom =% s,password =%s, email =%s, date_adhesion=%s, tel=%s,avatar_photo=%s  WHERE id =% s', (nom, prenom, password, email,date_adhesion, tel, (userId, ), ))
                mysql.connection.commit()
                msg = 'User updated !'
                return redirect(url_for('users'))
        elif request.method == 'POST':
            msg = 'Please fill out the form !'        
        return render_template("edit.html", msg = msg, editUser = editUser)
    return redirect(url_for('login'))
if __name__ == "__main__":
    app.run()