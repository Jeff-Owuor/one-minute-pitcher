from flask import render_template,request,redirect,url_for,abort
from ..models import User,Pitch,Upvote,Downvote,Comment
from . import main
from .forms import UpdateProfile,PitchForm,CommentsForm
from .. import db,photos
from flask_login import login_required, current_user

@main.route('/')
def index():

    '''
    View root page function that returns the index page and its data
    '''
    pitches = Pitch.query.all()
    lifestyle = Pitch.query.filter_by(category = 'Lifestyle').all() 
    food = Pitch.query.filter_by(category = 'Food').all()
    music = Pitch.query.filter_by(category = 'Music').all()
    return render_template("index.html",pitches = pitches, music = music, food = food, lifestyle = lifestyle)

@main.route('/pitch/new/<int:id>', methods=['GET','POST'])
@login_required
def new_comment(id):
    pitch = Pitch.query.filter_by(id=id).first()
    
    if pitch is None:
        abort(404)
        
    form = CommentsForm()
    if form.validate_on_submit():
        comments = form.comment_detail.data
        new_comment = Comment( comment_info=comments, pitch=pitch )
        new_comment.save_comment()
        return redirect(url_for('.single_pitch', id=pitch.id ))
    title = 'New Comment'
    return render_template('comments.html', title=title, comment_form=form)

@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()
    
    form = PitchForm()
    
    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)



@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form)

@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))

@main.route('/upvote/<int:id>',methods = ['POST','GET'])
@login_required
def upvote(id):
    new_vote = Upvote(user = current_user, pitch_id=id)
    new_vote.save()
    return redirect(url_for('main.index',id=id))


@main.route('/pitch', methods = ['POST','GET'])
@login_required
def new_pitch():
    form = PitchForm()
    if form.validate_on_submit():
        pitch = form.pitch.data
        category = form.category.data
        user_id = current_user._get_current_object().id
        new_pitch_dict = Pitch(pitch = pitch,user_id=user_id,category=category)
        new_pitch_dict.save_pitch()
        return redirect(url_for('main.index'))
        
    return render_template('pitch.html', form = form)
