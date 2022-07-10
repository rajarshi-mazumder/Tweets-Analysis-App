
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError, IntegerField
from wtforms.validators import DataRequired, Length, EqualTo, NumberRange


class UserForm(FlaskForm):
    username = StringField("Twitter Userame", validators=[
                           DataRequired(), Length(min=2, max=20)])
    email_id = StringField("Email address", validators=[
                           DataRequired()])
    submit = SubmitField("Submit")


class TwitterSearchForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    number_of_tweets = IntegerField("Number of Tweets", validators=[DataRequired(),
                                    NumberRange(min=1, max=2000)])
    submit = SubmitField("Submit")
