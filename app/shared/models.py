from werkzeug.security import generate_password_hash, check_password_hash
from .connection import db


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False, unique=True)
    slug = db.Column(db.String(255), nullable=False, unique=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    content = db.Column(db.UnicodeText, nullable=False)
    date = db.Column(db.Date, nullable=False)

    #relationship property
    category = db.relationship('Category', backref=db.backref('posts', lazy='dynamic'))


    def __repr__(self):
        return self.title


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)


    def __repr__(self):
        return self.name


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    pwdhash = db.Column(db.String(255), nullable=False)


    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.pwdhash = generate_password_hash(password)


    def check_password(self, password):
        return check_password_hash(self.pwdhash, password)


    def is_authenticated(self):
        return True


    def is_active(self):
        return True


    def is_anonymous(self):
        return False


    def get_id(self):
        return unicode(self.id)