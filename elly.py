from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
DATABASE="2m.db"
DEBUG=True
print("Hello ell")

app = Flask(__name__)
app.config.from_object(__name__)

@app.route('/')
def index():
    return render_template('t1.html')

if __name__ == '__main__':
    app.run()
