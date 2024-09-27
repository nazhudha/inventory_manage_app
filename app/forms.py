from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, PasswordField, SubmitField, SelectField, ValidationError
from wtforms.validators import DataRequired, Email, Length, NumberRange

from app.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    role = SelectField('Role', choices=[('admin', 'Admin'), ('regular', 'Regular User')], validators=[DataRequired()])
    submit = SubmitField('Register')

# This was added >> Validaiton rules?
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Username already exists. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Email already registered. Please use a different email address.')
    
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class EquipmentForm(FlaskForm):
    name = StringField('Equipment Name', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired(), NumberRange(min=1, max=10)])
    
    # Admins can assign the equipment to any user, but regular users cannot
    user = SelectField('Assign to User', coerce=int)

    submit = SubmitField('Add/Update Equipment')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user.choices = [(user.id, user.username) for user in User.query.all()]  # Admin will see this
