from datetime import datetime
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug import secure_filename
from subprocess import check_output,STDOUT,CalledProcessError 
import os,glob,re,string,random,tempfile

COMPILER = "fpc"

DATABASE="bolyai.db"
DEBUG=True
SECRET_KEY = 'development key'
UPLOAD_FOLDER = 'new'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','lpr','pas', 'pl'])
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
        return '<Problem %r>' % self.id



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
@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    session['logged_in'] = False
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
            session['username'] = q.username
            session['firstname'] = q.firstname
            session['lastname'] = q.lastname
            session['cls'] = q.cls.classname
            flash('You were logged in')
            return redirect(url_for('problem_select'))

    return render_template('login.html',error=error)



@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('login'))



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS



def save_file(file):
    d = {}
    d['ip']=request.remote_addr
    d['updir']=session['cls']
    d['lastname']=session['lastname']
    d['firstname']=session['firstname']
    filename = '{updir}/{ip}-{lastname}-{firstname}.pas'
    filename = filename.format(**d)
    session['filename'] = filename
    #filename = secure_filename(filename)
    if not os.path.isdir(d['updir']):
        os.mkdir(d['updir'])
    file.save(filename)
    


@app.route('/show_problem', methods=['GET', 'POST'])
def show_problem():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            save_file(file)
            return redirect(url_for('check_solution'))
    
    id=request.args.get('id', '')
    session['problem_id']=id
    compilesolution(id)

    q = Problem.query.filter_by(id=id).first()
    problemtext = q.problemtext
    return render_template('problem.html',problemtext=problemtext)



@app.route('/check_solution')
def check_solution():
    # TODO error + errmsg
    error=None
    filename = session['filename']

    (rv,output)=compile(filename)
    
    if rv != 0:
        error = 'A program nem fordult le! ' + output
        return render_template('check_result.html',error=error)
    
    error = runtest()
    
    if error == None:
        save_solution()
    return render_template('check_result.html',error=error)


def save_solution():
    problem = Problem.query.filter_by(id=session['problem_id']).first()
    user = User.query.filter_by(username=session['username']).first()
    sol = Solution(problem,user,datetime.utcnow())
    db.session.add(sol)
    db.session.commit()



def generate_random_file(n=80,nl=10,contents=string.printable):
    FNLENGTH = 8

    # rnl = (random.randint(0,nl),random.randint(0,nl))
    # rnl = (min(rnl),max(rnl))
    # rn = (random.randint(0,n),random.randint(0,n))
    # rn = (min(rn),max(rn))

    (f,filename) = tempfile.mkstemp(text=True)
    os.close(f)
    f=open(filename,'w')
    for j in range(nl):
        for i in range(n):
            f.write(random.choice(contents))
        if nl!=0: f.write('\n')
        
    f.close()
    return filename


    
def runtest():
    exename = session['filename'].split('.pas')[0]
    tf=tempfile.SpooledTemporaryFile()
    fn = generate_random_file()
    tf.write(bytes(fn,'UTF-8'))
    tf.seek(0)
    solution_output = check_output('./'+session['problem_id'],stdin=tf,stderr=STDOUT)
    tf.seek(0)
    rv = None
    try:
        output = check_output([exename],stdin=tf,stderr=STDOUT)
    except CalledProcessError as e:
        rv = 'A program nem futot le!\n{}'.format(e.output)
    finally:
        tf.close()
    if output != solution_output:
        t = 'A program nem a megfelelő eredményt adta.'
        t = t + 'Várt:{}Kapott:{}'
        rv = t.format(output.decode('UTF-8'),solution_output.decode('UTF-8'))
    os.remove(fn)
    return rv


# @app.route('/show_entries')
# def show_entries():
#     pattern =os.path.join(app.config['UPLOAD_FOLDER'],'*')
#     entries = glob.glob(pattern)
#     entries = map(lambda x : re.sub(app.config['UPLOAD_FOLDER']+'/?','',x), entries)
#     return render_template('show_entries.html', entries=entries)


@app.route('/problem_select')
def problem_select():
    if session['logged_in'] == True:
        q = Problem.query.all()
        ids = map(lambda x : x.id, q)
        return render_template('problem_select.html', ids=ids)
    return redirect(url_for('login'))

def compile(filename):
    print('Compiling {}'.format(filename))
    cmd = [COMPILER,filename]
    try:
        out = check_output(cmd,stderr=STDOUT)
        return (0,out.decode('UTF-8'))
    except CalledProcessError as e:
        return (e.returncode,e.output.decode('UTF-8'))

def compilesolution(id):
    fn = id+'.pas'
    if not os.path.exists(fn) or not os.access(fn, os.X_OK):
        compile(fn)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
