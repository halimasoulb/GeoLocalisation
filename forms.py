from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from datetime import datetime
import enum
from sqlalchemy import Enum


class CaseType(enum.Enum):
    NEW = "Confirme"
    RECOVERED = "Gueri"
    DEAD = "Decede"

class RegistrationForm(FlaskForm):
    prenom = StringField('Prenom',
                           validators=[DataRequired(), Length(min=2, max=20)], render_kw={"placeholder": "Mohamed"})
    nom = StringField('Nom',
                        validators=[DataRequired(), Length(min=2, max=20)], render_kw={"placeholder": "MERINI"})

    date = DateField('Date (optional)', format='%Y-%m-%d %H:%M:%S', default=datetime.today, render_kw={"placeholder": "1997-06-24"} )

    cin = StringField('CIN',
                           validators=[DataRequired(), Length(min=8, max=9)], render_kw={"placeholder": "xxxxxxxx"})
   
    submit = SubmitField('Enregistrer')


class ChangeStatus(FlaskForm):
	cin = StringField('CIN',
                           validators=[DataRequired(), Length(min=8, max=9)], render_kw={"placeholder": "xxxxxxxx"})

	etat = SelectField('Etat malade',
							choices=[(CaseType.RECOVERED.value), (CaseType.DEAD.value)], validators=[ DataRequired()])
	submit = SubmitField('Modifier')