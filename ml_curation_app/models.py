from ml_curation_app import db
from datetime import date, datetime
from flask import Flask
from sqlalchemy.sql.expression import false
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.sqltypes import FLOAT, INTEGER, Integer, VARCHAR ,String , Text
from sqlalchemy import UniqueConstraint # post-link unique 제약조건용

class Post(db.Model):
    __tablename__ = 'post'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.VARCHAR(170))
    body = db.Column(db.VARCHAR,nullable= False)
    pub_date = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow)
    
    blog_name = db.Column(db.String(200))
    post_link = db.Column(db.VARCHAR, unique = True)
    

    def __repr__(self):
        return f"Post {self.id}"


class Blog(db.Model):
    __tablename__ = 'blog'

    id = db.Column(db.Integer, primary_key = True)
    owner = db.Column(String)
    name = db.Column(String)
    rss = db.Column(String)
    link = db.Column(String)
    categories = db.Column(String)


    def __repr__(self):
        return f"Blog {self.id}"


""" class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(Integer())
    username = db.Column(String, unique=True)
    email = db.Column(String, unique=True)
    password = db.Column(String)


    def __repr__(self):
        return f"User {self.id}"
 """