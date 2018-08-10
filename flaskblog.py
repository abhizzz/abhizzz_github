
from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect, request
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm


app=Flask(__name__)
app.config['SECRET_KEY']='d11f922e0d92d08db891e6a6c52ce4d9'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'
db=SQLAlchemy(app)
	

class User(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	username=db.Column(db.String(20), unique=True, nullable=False)
	email=db.Column(db.String(120), unique=True, nullable=False)
	image_file=db.Column(db.String(20), nullable=False, default='default.jpg')
	password=db.Column(db.String(60),nullable =False)
	posts = db.relationship('Post',backref='author', lazy=True)
	
	def __repr__(self):
		return f"User('{self.username}','{self.email}','{self.image_file}')"


class Post(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	title=db.Column(db.String(100),nullable=False)
	date_posted=db.Column(db.DateTime,nullable=False, default=datetime.utcnow)
	content=db.Column(db.Text, nullable=False)
	user_id=db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	
	def __repr__(self):
		return f"Post('{self.title}','{self.date_posted}')"


	

posts=[
	{
		'author':'Abhishek Yadav',
		'title':'Blog Post 1',
		'content':'first post content',
		'date_posted':'April 20, 2011'
	},
	{
		'author':'allen walker',
		'title':'Blog Post 2',
		'content':'second post content',
		'date_posted':'April 22, 2012'
	}

]



@app.route("/")
@app.route("/home",methods=['GET','POST'])
def home():
	return render_template('home.html',posts='home')
	

@app.route("/Dashboard")
def Dashboard():
	return render_template('Dashboard.html',posts='Dashboard')
	
@app.route("/new")
def new():
	return render_template('new.html',posts='new')

@app.route("/settings")
def settings():
	return render_template('settings.html',posts='settings')

@app.route("/History")
def History():
	return render_template('History.html',posts='History')

	
@app.route("/generatebill", methods=['GET','POST'])
def generatebill():
	if request.method=="POST":
		return 'ok'
	kgs=range(1,100)
	unit_price=200
	user_item=7
	return render_template("generatebill.html",kgs=kgs,unit_price=unit_price,user_item=user_item)
	#return name_of_slider
	#return render_template(name_of_slider)
	
	
@app.route("/about")
def about():
	return render_template('about.html',title='About')
	
	
@app.route("/register", methods=['Get','Post'])
def register():
	form=RegistrationForm()
	if form.validate_on_submit():
		flash(f'Account Created for {form.username.date}!','success')
		return redirect(url_for('home'))
	return render_template('register.html',title='Register', form=form)
	

@app.route("/login", methods=['Get','Post'])
def login():
	form=LoginForm()
	if form.validate_on_submit():
		if form.email.data=='master@abhishek.com' and form.password.data=='password':
			flash(f'You have logged in!','success')
			#flash('You have logged in!','success')
			return redirect(url_for('home'))
		else: 
			flash(f'Login Uncessfull. Please check username and password ','danger')
	return render_template('login.html',title='login', form=form)
	
	
@app.route("/weight", methods=['Get','Post'])
def weight():
	form=WeightForm()
	if form.validate_on_submit():
		flash(f'we r through for {form.username.date}!','success')
		#return redirect(url_for('home'))
		return redirect(url_for('generatebill'))
	return render_template('generatebill.html',title='weight',form=form)
	
	


	

	
if __name__=='__main__':
	app.run(debug=True)