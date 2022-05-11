from flask_wtf import FlaskForm
from wtforms import TextAreaField,SubmitField, SelectField
from wtforms.validators import DataRequired

class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you.',validators = [DataRequired()])
    submit = SubmitField('Submit')
    
class PitchForm(FlaskForm):
    pitch = TextAreaField('Pitch', validators=[DataRequired()])
    category = SelectField('Category', choices=[('Lifestyle','Lifestyle'),('Food','Food'),('Music','Music')],validators=[DataRequired()])
    submit = SubmitField('Submit')
    
    
class CommentsForm(FlaskForm):
    comment_detail = TextAreaField('Comment', validators=[DataRequired()])
    submit = SubmitField('Submit')