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
    vote = db.relationship('Votes',backref='user',lazy='dynamic')
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
    
    def __repr__(self):
        return f'User {self.username}'
    
    
    
class Pitch(db.Model):
    
    __tablename__ = 'pitches'
    
    id = db.Column(db.Integer,primary_key = True)
    posted = db.Column(db.DateTime,default=datetime.utcnow)
    category = db.Column(db.String(255))
    pitch = db.Column(db.String())
    vote = db.relationship('Votes',backref='pitches',lazy='dynamic')
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    comment = db.relationship('Comment',backref = 'pitches',lazy="dynamic") 
    
    def save_pitch(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_pitches(cls,id):
        pitches = Pitch.query.filter_by(user_id=id).all()
        return pitches  
    
    def __repr__(self):
        return f'Pitch {self.pitch}'


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer,primary_key=True)
    comment = db.Column(db.Text(),nullable = False)
    time_posted = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'),nullable = False)
    pitch_id = db.Column(db.Integer,db.ForeignKey('pitches.id'))
    
    def save_comment(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_comments(self, id):
        comment = Comment.query.order_by(Comment.time_posted.desc()).filter_by(pitch_id=id).all()
        return comment

    
class Votes(db.Model):
    """
    class to model votes
    """
    __tablename__='votes'

    id = db.Column(db. Integer, primary_key=True)
    vote = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    pitches_id = db.Column(db.Integer, db.ForeignKey("pitches.id"))

    def save_vote(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_votes(cls,user_id,pitches_id):
        votes = Votes.query.filter_by(user_id=user_id, pitches_id=pitches_id).all()
        return votes

    def __repr__(self):
        return f'{self.vote}:{self.user_id}:{self.pitches_id}'    
   

  
class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(255))
    users = db.relationship('User',backref = 'role',lazy="dynamic")

    def __repr__(self):
        return f'User {self.name}'