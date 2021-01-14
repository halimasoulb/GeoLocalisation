from flask_wtf import FlaskForm
from wtforms import StringField, DateTimeField, SubmitField, SelectField, BooleanField, PasswordField, SubmitField, TextField, RadioField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp
from datetime import datetime
import enum
from sqlalchemy import Enum
from wtforms import ValidationError
from models import User
import json



class RegistrationForm(FlaskForm):
    prenom = StringField('Prenom',
                           validators=[DataRequired(), Length(min=2, max=20)], render_kw={"placeholder": "Prenom"})
    nom = StringField('Nom',
                        validators=[DataRequired(), Length(min=2, max=20)], render_kw={"placeholder": "NOM"})

    sexe = SelectField('Sexe', choices=[('1', 'Homme'), ('2', 'Femme')], validators=[ DataRequired()])
    
    date_de_naissance = DateTimeField("Date de naissance", format="%m/%d/%Y")

    cin = StringField('CIN', validators=[DataRequired(), Regexp('^[A-Z]{1,2}[0-9]{6}$')], render_kw={"placeholder": "AB123456"})

    date = DateTimeField("Date Declaration", id='datePicker', format="%m/%d/%Y")

    adresse = TextField('Adresse',validators=[DataRequired(), Length(min=3, max=100)], render_kw={"placeholder": "CENTRE BOUSKOURA PRES DYAR AYOUB"})

    residance = SelectField('Residant province', choices=[('1', 'oui'),('2', 'non')])

    employe = SelectField('Employe province', choices=[('1', 'oui'),('2', 'non')])

    id_societe = StringField('ID Societe', validators=[DataRequired(), Length(min=3, max=100)])

    nom_societe = StringField('Nom Societe',  validators=[DataRequired(), Length(min=3, max=100)])

    aal =  SelectField('AAL', choices=[], validators=[ DataRequired()])

    pachalik =  SelectField('PACHALIK', choices=[], validators=[ DataRequired()])

    observation = TextAreaField("Observation", render_kw={"placeholder": "Est sortie de l'hopital le 12/05/2020 mais toujours positive covid-19"} )
   
    submit = SubmitField('Enregistrer')

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        with open('config.js') as json_file:
            data = json.load(json_file)
            #for p in data["pachalik1"]: 
            self.pachalik.choices = [(i, i["pachalik1"]) for i in data["liste"]]
                #self.aal.choices = p



class ChangeStatus(FlaskForm):

    cin = StringField('CIN', validators=[DataRequired(), Regexp('^[A-Z]{1,2}[0-9]{6}$')], render_kw={"placeholder": "AB123456"})
    
    status = SelectField('Etat malade', choices=[], validators=[ DataRequired()])  

    date_hospitalisation = DateTimeField("Date Hospitalisation", id='datePicker', format="%m/%d/%Y")

    date_guerison = DateTimeField("Date guerison", id='datePicker', format="%m/%d/%Y")

    lieu_hospitalisation = TextField('Lieu Hospitalisation',validators=[DataRequired(), Length(min=3, max=100)], render_kw={"placeholder": "HOPITAL SEKKAT PREFECTURE D'ARRONDISSEMENT AIN CHOCK"})

    date_deces = DateTimeField("Date deces", id='datePicker', format="%m/%d/%Y")

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
    
    email = TextField('Email',
            validators=[DataRequired(), Email(), Length(min=6, max=40)], render_kw={"placeholder": "admin@gmail.com"})
    password = PasswordField('Mot de passe',
            validators=[DataRequired(), Length(min=8, max=20)], render_kw={"placeholder": "xxxxxxxx"})
    confirm = PasswordField('Verifier mot de passe',
            validators=[DataRequired(), EqualTo('password', message='mot de passe doit correspondre')], render_kw={"placeholder": "xxxxxxxx"})
    submit = SubmitField('Enregistrer')

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
