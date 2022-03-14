"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class Users(db.Model):
    __tablename__ = 'users'
    
    def __repr__(self):
        u = self
        return f"<User id={u.id} first_name={u.first_name} last_name={u.last_name}"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(2083))

class Posts(db.Model):
    __tablename__ = 'posts'

    def __repr__(self):
        p = self
        return f"Post id={p.id} title={p.title} content={p.content} created_at={p.created_at} user_id={p.user_id}"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.Text, default=datetime.datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

class Tags (db.Model):
    __tablename__ = 'tags'

    def __repr__(self):
        t = self
        return f"Tag id={t.id} name={t.name}"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, unique=True, nullable=False)

class PostTags (db.Model):
    __tablename__ = 'post_tags'

    def __repr__(self):
        pt = self
        return f"Post Tag post_id={pt.post_id} tag_id={pt.tag_id}"

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)
