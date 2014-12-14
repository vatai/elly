from elly import db,Cls,User

db.create_all()

cls = Cls('proba')
user = User('vatai', 'Vatai','Emil', 'pass123', cls)

db.session.add(cls)
db.session.add(user)
db.session.commit()
