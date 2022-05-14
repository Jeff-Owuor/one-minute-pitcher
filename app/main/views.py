from flask import render_template,request,redirect,url_for,abort
from ..models import User,Pitch,Votes,Comment
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

@main.route('/comments/<int:id>', methods=['GET','POST'])
@login_required
def new_comment(id):
    pitch = Pitch.query.filter_by(id=id).first()
    form = CommentsForm()
    if pitch is None:
        abort(404)
        
    
    if form.validate_on_submit():
        comments = form.comment_detail.data
        new_comment = Comment( comment=comments, user_id = current_user.id, pitch_id = pitch.id )
        new_comment.save_comment()
        return redirect(url_for('.a_pitch', id=pitch.id ))
    return render_template('comments.html',form=form)

@main.route('/a_pitch/<int:id>', methods=['GET', 'POST'])
@login_required
def a_pitch(id):
    pitches = Pitch.query.get(id)
    
    if pitches is None:
        abort(404)
    
    comment = Comment.get_comments(id)
    count_likes = Votes.query.filter_by(pitches_id=id, vote=1).all()
    count_dislikes = Votes.query.filter_by(pitches_id=id, vote=2).all()
    return render_template('a_pitch.html', pitches = pitches, comment = comment, count_likes=len(count_likes), count_dislikes=len(count_dislikes))

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

@main.route('/pitch/upvote/<int:id>&<int:vote_type>')
@login_required
def upvote(id,vote_type):
    votes = Votes.query.filter_by(user_id=current_user.id).all()
    print(f'The new vote is {votes}')
    to_str=f'{vote_type}:{current_user.id}:{id}'
    print(f'The current vote is {to_str}')

    if not votes:
        new_vote = Votes(vote=vote_type, user_id=current_user.id, pitches_id=id)
        new_vote.save_vote()
        print('YOU HAVE new VOTED')

    for vote in votes:
        if f'{vote}' == to_str:
            print('YOU CANNOT VOTE MORE THAN ONCE')
            break
        else:   
            new_vote = Votes(vote=vote_type, user_id=current_user.id, pitches_id=id)
            new_vote.save_vote()
            print('YOU HAVE VOTED')
            break
    return redirect(url_for('.a_pitch', id=id))   
    