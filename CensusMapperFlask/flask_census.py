from create_user import db
from create_user import User

#creates the initial db
db.create_all()

#creates user objects
admin = User('admin', 'admin@example.com')
guest = User('guest', 'guest@example.com')

#commits the new users to the db
db.session.add(admin)
db.session.add(guest)
db.session.commit()

#to access the user db
users = User.query.all()
admin = User.query.filter_by(username='admin').first()
