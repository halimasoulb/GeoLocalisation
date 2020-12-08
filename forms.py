from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp
from datetime import datetime
import enum
from sqlalchemy import Enum



class RegistrationForm(FlaskForm):
    prenom = StringField('Prenom',
                           validators=[DataRequired(), Length(min=2, max=20)], render_kw={"placeholder": "Mohamed"})
    nom = StringField('Nom',
                        validators=[DataRequired(), Length(min=2, max=20)], render_kw={"placeholder": "MERINI"})

    date = StringField("Date", id='datePicker')

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
