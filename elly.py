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

# import hashlib; hashlib.sha224('elteik').hexdigest()

@app.route('/')
def index():
    return render_template('t1.html')

if __name__ == '__main__':
    app.run()
