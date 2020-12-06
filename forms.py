from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from datetime import datetime
import enum
from sqlalchemy import Enum



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
    
    status = SelectField('Etat malade', choices=[], 
                        validators=[ DataRequired()])    

    submit = SubmitField('Modifier')

    def __init__(self, states, *args, **kwargs):
        super(ChangeStatus, self).__init__(*args, **kwargs)
        self.status.choices = states