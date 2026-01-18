from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin
# Import db from your config file instead of creating it here
from config import db

class Article(db.Model, SerializerMixin):
    __tablename__ = 'articles'

    # Add serialization rules to avoid infinite recursion with relationships
    serialize_rules = ('-user.articles',)

    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String)
    title = db.Column(db.String)
    content = db.Column(db.String)
    preview = db.Column(db.String)
    minutes_to_read = db.Column(db.Integer)
    date = db.Column(db.DateTime, server_default=db.func.now())

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return f'<Article {self.id} by {self.author}>'

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    # Add serialization rules to avoid infinite recursion
    serialize_rules = ('-articles.user',)

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True)

    articles = db.relationship('Article', backref='user', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<User {self.username}, ID {self.id}>'