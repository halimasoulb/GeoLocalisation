from flask_wtf import FlaskForm
from wtforms import StringField, DateTimeField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp
from wtforms import BooleanField, PasswordField, SubmitField, TextField
from datetime import datetime
import enum
from sqlalchemy import Enum
from wtforms import ValidationError
from models import User



class RegistrationForm(FlaskForm):
    prenom = StringField('Prenom',
                           validators=[DataRequired(), Length(min=2, max=20)], render_kw={"placeholder": "Prenom"})
    nom = StringField('Nom',
                        validators=[DataRequired(), Length(min=2, max=20)], render_kw={"placeholder": "NOM"})

    date = DateTimeField("Date", id='datePicker', format="%m/%d/%Y %H:%M %p")

    cin = StringField('CIN',
                           validators=[DataRequired(), Regexp('^[A-Z]{1,2}[0-9]{6}$')], render_kw={"placeholder": "AB123456"})
   
    submit = SubmitField('Enregistrer')


class ChangeStatus(FlaskForm):

    cin = StringField('CIN',
                           validators=[DataRequired(), Regexp('^[A-Z]{1,2}[0-9]{6}$')], render_kw={"placeholder": "xxxxxxxx"})
    
    status = SelectField('Etat malade', choices=[], 
                        validators=[ DataRequired()])    

    submit = SubmitField('Modifier')

    def __init__(self, states, *args, **kwargs):
        super(ChangeStatus, self).__init__(*args, **kwargs)
        self.status.choices = states


class LoginForm(FlaskForm):

    email = TextField('Email',
            validators=[DataRequired(), Length(1, 64), Email()], render_kw={"placeholder": "admin@gmail.com"})
    password = PasswordField('mot de passe', validators=[DataRequired()], render_kw={"placeholder": "xxxxxxxx"})
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Se connecter')

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)


class RegisterForm(FlaskForm):
    username = TextField('Pseudo',
            validators=[DataRequired(), Length(min=3, max=32)])
    email = TextField('Email',
            validators=[DataRequired(), Email(), Length(min=6, max=40)], render_kw={"placeholder": "admin@gmail.com"})
    password = PasswordField('Mot de passe',
            validators=[DataRequired(), Length(min=8, max=20)], render_kw={"placeholder": "xxxxxxxx"})
    confirm = PasswordField('Verifier mot de passe',
            validators=[DataRequired(), EqualTo('password', message='mot de passe doit correspondre')], render_kw={"placeholder": "xxxxxxxx"})
    submit = SubmitField('Enregistrer')

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
