from app.routes import db, session, Base


class Users(Base):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), nullable=False)
    department = db.Column(db.String(250), nullable=False)
    date_joined = db.Column(db.String(250), nullable=False)

    def __init__(self, id, username, email, department, date_joined):
        self.id = id
        self.username = username
        self.email = email
        self.department = department
        self.date_joined = date_joined

    def __str__(self):
        return f'id: {self.id}, username: {self.username}'

    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'department': self.department,
            'date_joined': self.date_joined,
        }
