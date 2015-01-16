from unidecode import unidecode
from datetime import datetime,date
from os import remove
remove("bolyai.db")

from ignored import problems
from elly import *
db.app = app
db.init_app(app)

db.create_all()

cls = Cls('proba')
db.session.add(cls)

user = User('vatai', 'Vatai','Emil', 'pass123', cls)
db.session.add(user)

problem = Problem(problems[0],cls,date(2015,1,15))
db.session.add(problem)

solution = Solution(problem, user, datetime.utcnow())
db.session.add(solution)

db.session.commit()


lista=[['Ali', 'Arszen'],
   ['Bencsik', 'Blanka'],
   ['Bozsóki', 'Andor'],
   ['Bódi', 'Viktor'],
   ['Csipak', 'Noémi'],
   ['Fehér', 'Krisztián'],
   ['Fenyvesi', 'Abigél'],
   ['Fodor', 'Ádám'],
   ['Gajda', 'Benedek'],
   ['Galusz', 'Márton'],
   ['Gulyás', 'Nikoletta'],
   ['Kovács', 'Noel'],
   ['Lukács', 'Máté'],
   ['Szögi', 'Evelin'],
   ['Toldi', 'Teodóra'],
   ['Tóth', 'Koppány'],
   ['Vrbaški', 'Viktor']]

cls = Cls('2m')
db.session.add(cls)

lista=map(lambda x : [unidecode(x[0]).lower(),x[0],x[1],'pass',cls],lista)
for s in lista:
    user = User(*s)
    db.session.add(user)



y = [['Almási', 'Csilla'],
     ['Bedleg', 'Kristóf'],
     ['Berze', 'Tamás'],
     ['Csipak', 'Levente'],
     ['Gajda', 'Gergely'],
     ['Juhász', 'Kristóf'],
     ['Karácsonyi', 'Ágnes'],
     ['Kiss', 'Tamás'],
     ['Kormányos', 'Gergő'],
     ['Petrás', 'Ármin'],
     ['Rekalija', 'Roland'],
     ['Rozsnyik', 'Szabolcs'],
     ['Szakály', 'László'],
     ['Széll', 'Réka'],
     ['Szvoreny', 'Tamara'],
     ['Téglás', 'Ervin'],
     ['Tűri', 'Erik'],
     ['Utasi', 'Arnold'],
     ['Vrábel', 'Máté']]

cls = Cls('4m')
db.session.add(cls)

y=map(lambda x : [unidecode(x[0]).lower()+'4m',x[0],x[1],'pass',cls],y)
for s in y:
    user = User(*s)
    db.session.add(user)

db.session.commit()
