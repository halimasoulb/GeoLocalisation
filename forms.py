from flask_wtf import FlaskForm
from wtforms import StringField, DateTimeField, SubmitField, SelectField, BooleanField, PasswordField, SubmitField, TextField, RadioField, TextAreaField, DateField, validators
from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp
from wtforms.fields.html5 import DateTimeLocalField
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
    
    date_de_naissance = DateTimeLocalField("Date de naissance", validators=[ DataRequired()],  format='%Y-%m-%dT%H:%M')

    cin = StringField('CIN', validators=[DataRequired(), Regexp('^[A-Z]{1,2}[0-9]{6}$')], render_kw={"placeholder": "AB123456"})

    date = DateTimeLocalField("Date Declaration", validators=[ DataRequired()], format='%Y-%m-%dT%H:%M' )

    adresse = TextField('Adresse',validators=[DataRequired(), Length(min=3, max=100)], render_kw={"placeholder": "CENTRE BOUSKOURA PRES DYAR AYOUB"})

    residance = SelectField('Residant province', choices=[('1', 'oui'),('2', 'non')])

    employe = SelectField('Employe province', choices=[('1', 'oui'),('2', 'non')])

    id_societe = StringField('ID Societe', validators=[validators.Optional()])

    nom_societe = StringField('Nom Societe', validators=[validators.Optional()])

    aal =  SelectField('AAL', choices=[])

    pachalik =  SelectField('PACHALIK', choices=[])

    observation = TextAreaField("Observation", render_kw={"placeholder": "Est sortie de l'hopital le 12/05/2020 mais toujours positive covid-19"} )
   
    submit = SubmitField('Enregistrer')

    """def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        with open('config.json') as json_file:
            data = json.loads(json_file.read())
            for d in data: 
                if d["parent_id"] == 0:
                    self.pachalik.choices = [(i, i[1]) for i in d]"""



class ChangeStatus(FlaskForm):

    cin = StringField('CIN', validators=[DataRequired(), Regexp('^[A-Z]{1,2}[0-9]{6}$')], render_kw={"placeholder": "AB123456"})
    
    status = SelectField('Etat malade', choices=[], validators=[ DataRequired()])  

    date_hospitalisation = DateTimeLocalField("Date Hospitalisation", format='%Y-%m-%dT%H:%M',  validators=[validators.Optional()])

    date_guerison = DateTimeLocalField("Date guerison", format='%Y-%m-%dT%H:%M',  validators=[validators.Optional()])

    lieu_hospitalisation = TextField('Lieu Hospitalisation', validators=[validators.Optional()], render_kw={"placeholder": "HOPITAL SEKKAT PREFECTURE D'ARRONDISSEMENT AIN CHOCK"})

    date_deces = DateTimeLocalField("Date deces", validators=[validators.Optional()], format='%Y-%m-%dT%H:%M')

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



