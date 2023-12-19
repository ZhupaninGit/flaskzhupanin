from app import db,login_manager,bcrypt
from flask_login import UserMixin
import datetime
import enum

@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(int(user_id))

class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100),unique=True,nullable=False)
    email = db.Column(db.String(100),unique=True,nullable=False)
    about_me = db.Column(db.String(255)) 
    last_seen = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    image = db.Column(db.String(100),default="default.jpg")
    password = db.Column(db.String(255), nullable=False)

    def __init__(self,username,email,password):
        self.username = username
        self.email = email
        self.password = bcrypt.generate_password_hash(password)

class EnumPost(enum.Enum):
    news = "News"
    events = "Events"
    blog =  "Blog"
    other = "Other"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100),nullable=False)
    text = db.Column(db.Text(),nullable=False)
    image = db.Column(db.String(100),default="default.jpg")
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    type = db.Column(db.Enum(EnumPost), default='other')
    enabled = db.Column(db.Boolean(),default=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category', backref='posts')
    
    def __repr__(self):
        return f"<Post {self.id}: {self.title},{self.type}>"


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

post_tags = db.Table('post_tags',
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True)
)

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    posts = db.relationship('Post', secondary=post_tags, backref='tags')