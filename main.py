
from flask import Flask,session,redirect,render_template,url_for,request,flash
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,validators,TextAreaField
from wtforms.validators import DataRequired,Email,Length
from wtforms.fields.html5 import EmailField
from flask_pure import Pure
import sqlite3 as sql
from werkzeug.security import generate_password_hash,check_password_hash
from flask_simplemde import SimpleMDE




app=Flask(__name__,static_url_path = "/image" ,static_folder = "image")
app.config['SECRET_KEY']='super secret key'
Pure(app)
app.config['SIMPLEMDE_JS_IIFE'] = True
app.config['SIMPLEMDE_USE_CDN'] = True
SimpleMDE(app)




class Sign(FlaskForm):
	username = StringField('Username',validators=[DataRequired()])
	email = EmailField('Email',[validators.DataRequired(), validators.Email()])	
	password = PasswordField('Password',[validators.DataRequired()])




@app.route('/sign')
def sign():
	form=Sign()
	return render_template('sign.html',form=form,username=session.get('username'))





class Login(FlaskForm):
	username = StringField('Username',validators=[DataRequired()])
	password = PasswordField('password',validators=[DataRequired()])





@app.route('/permision',methods=['POST','GET'])
def permision():

	if request.method == 'POST':
		username = request.form['username']
		email = request.form['email']
		password = generate_password_hash(request.form['password'])
		with sql.connect('pro.db') as con:

			cur = con.cursor()
			cur.execute('SELECT * FROM pro WHERE username = ? AND email = ?',[username,email])
			con.commit()
			x = cur.fetchall()
			if  x:
				flash( ' Data already exist ' )
				return redirect(url_for('sign'))
			else:
				cur.execute('INSERT INTO pro (username,email,password) VALUES(?,?,?)',[username,email,password])
				con.commit()
				return redirect(url_for('permision'))
				con.close()
	return render_template('permision.html')





@app.route('/login',methods=['POST','GET'])
def login():
	form2 = Login()
	if request.method == 'POST':
		session['username'] = request.form['username']
		return redirect(url_for('home'))
	return render_template('login.html',form2=form2,username=session.get('username'))




@app.route('/Welcome+In+NOTO?/*-Application', methods=['POST','GET'])
def home():
	form2 = Login()
	form4 = Update()
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		with sql.connect('pro.db') as con:
			cur = con.cursor()
			cur.execute('SELECT password FROM pro WHERE username = ? ',[username])
			con.commit()
			x = cur.fetchall()
			if x and check_password_hash(x[0][0],password):	
				session['username'] = username
				if 'username' in session:
					username = session['username']
					return redirect(url_for('home'))
			else:
				flash('Data is not valid')
				return redirect(url_for('login'))
				con.close()



	with sql.connect('pro.db') as conn:
		conn.row_factory = sql.Row
		cur = conn.cursor()
		username = session.get('username')
		cur.execute(' SELECT * from data WHERE  username = ? ',[username])
		row = cur.fetchall();

	return render_template('home.html',username = session.get('username'),row=row,form2=form2,form4=form4)
	



class Notes(FlaskForm):
	title = StringField('title',validators=[DataRequired()]) 
	note = TextAreaField('note',validators=[DataRequired()])




@app.route('/logout')
def logout():
	session.pop('username',None)
	return redirect(url_for('login'))






@app.route('/notes + maker + Application')
def notes():
	form3 = Notes()
	return render_template('note.html',form3=form3,username = session.get('username'))







@app.route('/confirm',methods=['POST','GET'])
def confirm():
	form3 = Notes()
	if request.method == 'POST':
		title = request.form['title']
		note = request.form['note']
		username = session.get('username')
		with sql.connect('pro.db') as con:
			cur = con.cursor()
			cur.execute('INSERT INTO data (title,note,username) VALUES(?,?,?)',[title,note,username])
			con.commit()
			return redirect(url_for('home'))
			con.close()
	return render_template('confirm.html')





@app.route('/data/<id>',methods=['GET'])
def data(id,**kwargs):
	with sql.connect('pro.db') as conn:
		conn.row_factory = sql.Row
		cur = conn.cursor()
		username = session.get('username')
		cur.execute(' SELECT * FROM data WHERE id = ?',[id])
		row = cur.fetchall();
	return render_template('data.html',username = session.get('username'),row=row)






@app.route('/delete/<id>')
def Delete(id, **kwargs):

	with sql.connect('pro.db') as conn:
		cur = conn.cursor()
		cur.execute(' DELETE FROM data WHERE id = ? ',[id])
		conn.commit()
		return redirect(url_for('home'))
		conn.close()





class Update(FlaskForm):
	title = StringField('title',validators=[DataRequired()]) 
	note = TextAreaField('note',validators=[DataRequired()])





@app.route('/update/<id>')
def update(id, **kwargs):

	form4 = Update()

	with sql.connect('pro.db') as conn:
		conn.row_factory = sql.Row
		cur = conn.cursor()
		username = session.get('username')
		cur.execute(' SELECT * FROM data WHERE id = ?',[id])
		row = cur.fetchall();
	return render_template('update.html',form4=form4,username = session.get('username'),row=row)





@app.route('/ti/<id>')
def ch(id,**kwargs):
	form4=Update()
	with sql.connect('pro.db') as conn:
		conn.row_factory = sql.Row
		cur = conn.cursor()
		username = session.get('username')
		cur.execute(' SELECT * FROM data WHERE id = ?',[id])
		row = cur.fetchall();
	return render_template('title.html',form4=form4,row=row,username=session.get('username'))






@app.route('/save/<id>',methods=['POST','GET'])
def save(id,**kwargs):
	if request.method == 'POST':
		#title = request.form['title']
		note = request.form['note']
		username = session.get('username')
		with sql.connect('pro.db') as conn:
			conn.row_factory = sql.Row
			cur = conn.cursor()
			username = session.get('username')
			cur.execute(' SELECT * FROM data WHERE id = ?',[id])
			row = cur.fetchall();
			for i in row:
				if i['id']:
					cur.execute(' UPDATE data SET note=? WHERE id = ? ',[note,id])
					return redirect(url_for('home'))
	return render_template('take.html')





@app.route('/title-update/<id>',methods=['POST','GET'])
def title(id,**kwargs):
	if request.method == 'POST':
		title = request.form['title']
		username = session.get('username')
		with sql.connect('pro.db') as conn:
			conn.row_factory = sql.Row
			cur = conn.cursor()
			username = session.get('username')
			cur.execute(' SELECT * FROM data WHERE id = ?',[id])
			row = cur.fetchall();
			for i in row:
				if i['id']:
					cur.execute(' UPDATE data SET title=? WHERE id = ? ',[title,id])
					return redirect(url_for('home'))
	return render_template('take.html')


if __name__=='__main__':
	app.run(debug=True)
