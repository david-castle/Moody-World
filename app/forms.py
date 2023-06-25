
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms_components import IntegerField
from wtforms.validators import DataRequired, Optional, NumberRange

# class LoginForm(FlaskForm):
#     username = StringField('Username', validators=[DataRequired()])
#     password = PasswordField('Password', validators=[DataRequired()])
#     remember_me = BooleanField('Remember Me')
#     submit = SubmitField('Sign In')

class QueryEditForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])

    hashtag = StringField("Hashtag", validators=[DataRequired()])

    number_results = IntegerField(
        "number_results",
        validators=[
            Optional(),
            NumberRange(min=1, max=500)
        ]
    )
