from unicodedata import category
from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from . import login_manager
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255))
    email = db.Column(db.String(255),unique = True,index = True)
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    upvote = db.relationship('Upvote',backref='user',lazy='dynamic')
    downvote = db.relationship('Downvote',backref='user',lazy='dynamic')
    pass_secure= db.Column(db.String(255))
    pitch = db.relationship('Pitch',backref = 'user',lazy="dynamic")
    
    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.pass_secure = generate_password_hash(password)


    def verify_password(self,password):
        return check_password_hash(self.pass_secure,password)
    
    def like_post(self, post):
        if not self.has_liked_post(post):
            like = Upvote(user_id=self.id, post_id=post.id)
            db.session.add(like)

    
    def has_liked_post(self, post):
        return Upvote.query.filter(
            Upvote.user_id == self.id,
            Upvote.pitch_id == post.id).count() > 0

     
    def __repr__(self):
        return f'User {self.username}'
    
    
    
class Pitch(db.Model):
    
    __tablename__ = 'pitches'
    
    id = db.Column(db.Integer,primary_key = True)
    posted = db.Column(db.DateTime,default=datetime.utcnow)
    category = db.Column(db.String(255))
    pitch = db.Column(db.String())
    upvote = db.relationship('Upvote',backref='pitch',lazy='dynamic')
    downvote = db.relationship('Downvote',backref='pitch',lazy='dynamic')
    user_id = db.Column(db.Integer,db.ForeignKey('users.id')) 
    
    def save_pitch(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_pitches(cls,id):
        pitches = Pitch.query.filter_by(user_id=id).all()
        return pitches  
    
    def __repr__(self):
        return f'Pitch {self.pitch}'

    
class Upvote(db.Model):
    __tablename__ = 'upvotes'

    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    pitch_id = db.Column(db.Integer,db.ForeignKey('pitches.id'))
    
    
    @classmethod
    def get_upvotes(cls,upvotes_id):
        upvote = Upvote.query.filter_by(pitch_id=upvotes_id).all()
        return upvote


    def __repr__(self):
        return f'{self.user_id}:{self.pitch_id}'
    

class Downvote(db.Model):
    __tablename__ = 'downvotes'

    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    pitch_id = db.Column(db.Integer,db.ForeignKey('pitches.id'))
    

    def save(self):
        db.session.add(self)
        db.session.commit()
    @classmethod
    def get_downvotes(cls,downvote_id):
        downvote = Downvote.query.filter_by(pitch_id=downvote_id).all()
        return downvote

    def __repr__(self):
        return f'{self.user_id}:{self.pitch_id}'

  
class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(255))
    users = db.relationship('User',backref = 'role',lazy="dynamic")

    def __repr__(self):
        return f'User {self.name}'