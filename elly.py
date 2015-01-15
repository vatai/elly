from datetime import datetime
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from werkzeug import secure_filename

from models import *
from tests import *

DATABASE="bolyai.db"
DEBUG=True
SECRET_KEY = 'development key'
UPLOAD_FOLDER = 'new'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg',
                          'gif','lpr','pas', 'pl'])
print('Elly started')


app = Flask(__name__)
app.config.from_object(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + DATABASE
db.init_app(app)


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
    
    # 1. compile
    (rv,output)=compile_pas(filename)
    
    if rv != 0:
        error = 'A program nem fordult le! ' + output
        return render_template('check_result.html',error=error)
    
    # 2. run test
    error = runtest(session)
    
    if error == None:
        save_solution()
    return render_template('check_result.html',error=error)


def save_solution():
    problem = Problem.query.filter_by(id=session['problem_id']).first()
    user = User.query.filter_by(username=session['username']).first()
    sol = Solution(problem,user,datetime.utcnow())
    db.session.add(sol)
    db.session.commit()


@app.route('/problem_select')
def problem_select():
    if session['logged_in'] == True:
        q = Problem.query.all()
        ids = map(lambda x : x.id, q)
        return render_template('problem_select.html', ids=ids)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(host='0.0.0.0')
