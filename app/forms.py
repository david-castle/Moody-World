from app.models import User
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms_components import IntegerField
from wtforms.validators import (DataRequired, Email, EqualTo, Optional, 
                                NumberRange, ValidationError)

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class QueryEditForm(FlaskForm):
    #name = StringField("Query Name", validators=[DataRequired()])
    searchtermsAny = StringField("Match Any of These Terms")#, validators=[DataRequired()])
    searchtermsAll = StringField("Match All of These Terms")#, validators=[DataRequired()])
    
    def validate(self, extra_validators=None):
        if super().validate(extra_validators):

            # your logic here e.g.
            if not (self.searchtermsAny.data or self.searchtermsAll.data):
                self.searchtermsAny.errors.append('At least one field must have a value')
                return False
            else:
                return True

        return False
    
    #number_results = IntegerField(
    #    "number_results",
    #    validators=[
    #        Optional(),
    #        NumberRange(min=1, max=100)
    #    ]
    #)

class RegistrationForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')
        
class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Request Password Reset')