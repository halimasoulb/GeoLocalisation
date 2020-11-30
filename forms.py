from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from datetime import datetime


class RegistrationForm(FlaskForm):
    prenom = StringField('Prenom',
                           validators=[DataRequired(), Length(min=2, max=20)], render_kw={"placeholder": "Mohamed"})
    nom = StringField('Nom',
                        validators=[DataRequired(), Length(min=2, max=20)], render_kw={"placeholder": "MERINI"})

    date = DateField('Date (optional)', format='%Y-%m-%d %H:%M:%S', default=datetime.today, render_kw={"placeholder": "1997-06-24"} )

    lieu_de_naissance =  StringField('Lieu de naissance', 
    					validators=[DataRequired(), Length(min=2, max=20)], render_kw={"placeholder": "Casablanca"}) 
    cin = StringField('CIN',
                           validators=[DataRequired(), Length(min=8, max=9)], render_kw={"placeholder": "xxxxxxxx"})
   
    submit = SubmitField('Enregistrer')