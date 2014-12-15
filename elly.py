from datetime import datetime
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug import secure_filename
import os 
import glob


DATABASE="bolyai.db"
DEBUG=True
SECRET_KEY = 'development key'
UPLOAD_FOLDER = 'pas'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','lpr','pas'])
print('Elly started')



app = Flask(__name__)
app.config.from_object(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + DATABASE
db = SQLAlchemy(app)



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    lastname = db.Column(db.String(30))
    firstname= db.Column(db.String(30))
    password = db.Column(db.String(60))
    cls_id   = db.Column(db.Integer, db.ForeignKey('cls.id'))
    cls      = db.relationship('Cls', backref=db.backref('students', lazy='dynamic'))

    def __init__(self, username, lastname, firstname, password, cls):
        self.username = username
        self.lastname = lastname
        self.firstname= firstname
        self.password = password
        self.cls = cls

    def __repr__(self):
        return '<User %r>' % self.username



class Cls(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    classname = db.Column(db.String(10), unique=True)

    def __init__(self, classname):
        self.classname = classname

    def __repr__(self):
        return '<Class %r>' % self.classname



class Problem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    problemtext = db.Column(db.Text)
    testtext    = db.Column(db.Text)
    cls_id   = db.Column(db.Integer, db.ForeignKey('cls.id'))
    cls      = db.relationship('Cls', backref=db.backref('problems', lazy='dynamic'))

    def __init__(self, problemtext, cls):
        self.problemtext = problemtext
        self.cls = cls

    def __repr__(self):
        return '<Problem %r>' % self.username



class Solution(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recorded  = db.Column(db.DateTime)
    user_id   = db.Column(db.Integer, db.ForeignKey('user.id'))
    user      = db.relationship('User', backref=db.backref('solutions', lazy='dynamic'))
    problem_id   = db.Column(db.Integer, db.ForeignKey('problem.id'))
    problem      = db.relationship('Problem', backref=db.backref('solutions', lazy='dynamic'))

    def __init__(self, problem, user, recorded):
        self.problem = problem
        self.user    = user
        self.recorded= recorded

    def __repr__(self):
        return '<Solution %r>' % self.username



# import hashlib; hashlib.sha224('elteik').hexdigest()
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        q = User.query.filter_by(username=username).first()
        if not q:
            error = 'Invalid username'
        elif q.password != password:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_problem'))

    return render_template('login.html',error=error)



@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('login'))



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def show_problem():
    if request.method == 'POST':
        file = request.files['file']
        ip = request.remote_addr
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], ip+filename))
            return redirect(url_for('show_entries',
                                    filename='finished'))
    return render_template('problem.html')



@app.route('/show_entries')
def show_entries():
    entries = glob.glob('pas/*')
    print entries
    return render_template('show_entries.html', entries=entries)

if __name__ == '__main__':
    app.run()
