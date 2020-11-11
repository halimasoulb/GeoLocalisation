from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class RegistrationForm(FlaskForm):
    prenom = StringField('Prenom',
                           validators=[DataRequired(), Length(min=2, max=20)], render_kw={"placeholder": "Mohamed"})
    nom = StringField('Nom',
                        validators=[DataRequired(), Length(min=2, max=20)], render_kw={"placeholder": "MERINI"})

    date_de_naissance = DateField('Date de naissance', format='%Y-%m-%d', render_kw={"placeholder": "1997-06-24"} )

    lieu_de_naissance =  StringField('Lieu de naissance', 
    					validators=[DataRequired(), Length(min=2, max=20)], render_kw={"placeholder": "Casablanca"}) 
    cin = StringField('CIN',
                           validators=[DataRequired(), Length(min=8, max=9)], render_kw={"placeholder": "xxxxxx"})
    
    submit = SubmitField('Enregistrer')