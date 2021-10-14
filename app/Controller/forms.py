from enum import unique
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField, PasswordField, BooleanField
from wtforms.validators import  DataRequired, Length, ValidationError, EqualTo, Email
from wtforms_sqlalchemy.fields import QuerySelectMultipleField
from wtforms.widgets import CheckboxInput, ListWidget

from app.Model.models import Post, Tag, User

def get_tags():
    return Tag.query.all()

def get_taglabel(thetag):
    return thetag.name

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    body = TextAreaField('Post Message', [Length(min=1, max=1500)])
    happiness_level = SelectField('Happiness Level',choices = [(3, 'I can\'t stop smiling'), (2, 'Really happy'), (1,'Happy')])
    tag = QuerySelectMultipleField( 'Tag', query_factory=get_tags , get_label=get_taglabel, widget=ListWidget(prefix_label=False), 
      option_widget=CheckboxInput() )
    submit = SubmitField('Post')

class SortForm(FlaskForm):
    select = SelectField('Select',choices = [(3,'Date'),(2,'Title'),(1,'# of likes'),(0,'Happiness level')])
    usersposts = BooleanField('Display my posts only.')
    submit = SubmitField('Refresh')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self,username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('The username already exists! Please use a different username.')

    # def validate_email(self,email):
    #     user = User.query.filter_by(email=email.data).first()
    #     if user is not None:
    #         raise ValidationError('The email already exists! Please use a different email address.')