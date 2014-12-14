from datetime import datetime
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from flask.ext.sqlalchemy import SQLAlchemy

DATABASE="bolyai.db"
DEBUG=True
print('Elly started')


app = Flask(__name__)
app.config.from_object(__name__)
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

@app.route('/')
def index():
    return render_template('t1.html')

if __name__ == '__main__':
    app.run()
