from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, BooleanField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log In')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(),
        Length(min=3, max=80)
    ])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=6)
    ])
    password2 = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match')
    ])
    submit = SubmitField('Register')

class PrayerRequestForm(FlaskForm):
    title = StringField('Title', validators=[
        DataRequired(),
        Length(min=5, max=200)
    ])
    content = TextAreaField('Prayer Request', validators=[
        DataRequired(),
        Length(min=10)
    ])
    category = SelectField('Category', choices=[
        ('Family', 'Family'),
        ('Health', 'Health'),
        ('Finances', 'Finances'),
        ('Relationships', 'Relationships'),
        ('Grief', 'Grief'),
        ('Gratitude', 'Gratitude / Thanksgiving')
    ], validators=[DataRequired()])
    bible_verse = TextAreaField('Bible Verse (Optional)')
    is_anonymous = BooleanField('Submit Anonymously')
    is_private = BooleanField('Make Private (Link-only)')
    is_urgent = BooleanField('Mark as Urgent')
    submit = SubmitField('Submit Prayer Request')

class PrayerNoteForm(FlaskForm):
    prayer_note = TextAreaField('Prayer Note (Optional)', validators=[Length(max=500)])
    is_private = BooleanField('Keep Note Private')
    submit = SubmitField('Submit Prayer')

class EncouragementForm(FlaskForm):
    content = TextAreaField('Encouragement Message', validators=[
        DataRequired(),
        Length(min=5, max=1000)
    ])
    bible_verse = TextAreaField('Bible Verse (Optional)')
    submit = SubmitField('Share Encouragement')
