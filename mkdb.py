from datetime import datetime
from elly import db,Cls,User,Problem,Solution

db.create_all()

cls = Cls('proba')
db.session.add(cls)

user = User('vatai', 'Vatai','Emil', 'pass123', cls)
db.session.add(user)

problem = Problem('irj egy programot',cls)
db.session.add(problem)

solution = Solution(problem, user, datetime.utcnow())
db.session.add(solution)

db.session.commit()
