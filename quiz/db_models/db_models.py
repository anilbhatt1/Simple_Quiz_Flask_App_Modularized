from datetime import datetime
from flask_login import UserMixin
from quiz import db
from werkzeug.security import generate_password_hash, check_password_hash

#Create Model to register users
class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    role = db.Column(db.String(20),nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    # Password stuff...
    password_hash = db.Column(db.String(128))
    # User can create many questions
    questions = db.relationship('Questions', backref='qn_creator')
    # This establishes a logical relationship between user and questions for each question created
    #quizlogs = db.relationship('Quizlogs', backref='quiz_taker')
    # This establishes a logical relationship between user and quiz logs for each attempt of quiz taken

    @property
    def password(self):
        print('trying to read pwd')
        raise AttributeError('Password is not a readable item !')

    @password.setter
    def password(self, password):
        print('Inside pwd setter', password)
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        print('Inside verify pwd', password)
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<Name %r>' % self.name

# Create model to store questions
class Questions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(500), nullable=False)
    question_type = db.Column(db.String(20), nullable=False)
    question_category = db.Column(db.String(30), nullable=False)
    choice1 = db.Column(db.String(150))
    choice2 = db.Column(db.String(150))
    choice3 = db.Column(db.String(150))
    choice4 = db.Column(db.String(150))
    choice5 = db.Column(db.String(150))
    image1 = db.Column(db.String(150))  # Only location of images will be saved in DB
    image2 = db.Column(db.String(150))  # image1, 2,...columns will be occupied only if question type involves image/s
    image3 = db.Column(db.String(150))
    image4 = db.Column(db.String(150))
    image5 = db.Column(db.String(150))
    answer = db.Column(db.String(20), nullable=False)
    other_answer = db.Column(db.String(250))
    active_flag = db.Column(db.String(10))  #'Active' & 'Inactive'
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    qn_creator_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    # users.id -> u is in small case because 'Users' table will be loaded in DB as 'users'