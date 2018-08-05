from flask import Flask,session,redirect,render_template,flash,request,url_for
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField
from wtforms.validators import DataRequired,Email
from werkzeug.security import generate_password_hash,check_password_hash
from wtforms.fields.html5 import EmailField
from flask_pure import Pure
import sqlite3 as sql



app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'
Pure(app)

class Sign(FlaskForm):
    username = StringField('username',validators=[DataRequired()])
    email = EmailField("Email", [DataRequired("Please enter your email address."), Email("Please enter your email address.")])
    password = PasswordField('password',validators=[DataRequired()])

@app.route('/sign')
def sign():
    form = Sign()
    return render_template('sign.html',form=form)

@app.route('/save', methods=['POST','GET'])
def save():
    if request.method == 'POST' and form.validate():
        username = request.form['username']
        email = request.form['email']
        hash = generate_password_hash(request.form['password'])
        password = hash
        with sql.connect('pro.db') as con:
            cur = con.cursor()
            cur.execute('SELECT * FROM pro WHERE username= ? AND email = ?',[username,email])
            con.commit()
            x = cur.fetchall()
            if x:
                #flash
                return redirect(url_for('sign'))
            else:
                cur.execute('INSERT INTO pro(username,email,password)VALUES(?,?,?)',[username,email,password])
                con.commit()
                return redirect(url_for('login'))
                con.close()


class Login(FlaskForm):
    username = StringField('username',validators=[DataRequired()])
    password = PasswordField('password',validators=[DataRequired()])


@app.route('/login',methods=['POST','GET'])
def login():
    form2 = Login()
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('home'))
    return render_template('login.html',form2=form2)


@app.route('/home', methods=['POST','GET'])
def home():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        with sql.connect('pro.db') as con:
            cur = con.cursor()
            cur.execute('SELECT password FROM pro WHERE username= ?',[username])
            con.commit()
            x = cur.fetchone()
            session['username'] = username
            if x and check_password_hash(x[0],password) == True:
                if 'username' in session:
                    username = session['username']
                    return redirect(url_for('home'))
                return redirect(url_for('login'))
                con.close()

    return render_template('home.html',username = session.get('username'))

@app.route('/logout')
def logout():
   # remove the username from the session if it is there
   session['logged_in'] = False
   session.pop('username', None)
   return login()

@app.route('/notes')
def notes():
    return 'notes'

@app.route('/setting')
def setting():
    return 'notes'

@app.route('/about')
def about():
    return 'notes'

@app.route('/contact')
def contact():
    return 'notes'

if __name__=='__main__':
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug = True)
