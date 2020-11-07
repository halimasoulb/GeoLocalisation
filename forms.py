from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class RegistrationForm(FlaskForm):
    prenom = StringField('Prenom',
                           validators=[DataRequired(), Length(min=2, max=20)], render_kw={"placeholder": "Mohamed"})
    nom = StringField('Nom',
                        validators=[DataRequired(), Length(min=2, max=20)], render_kw={"placeholder": "Merini"})
    age =  StringField('Age', 
    					validators=[DataRequired(), Length(min=1, max=3)], render_kw={"placeholder": "30"})
    lieu_de_naissance =  StringField('Lieu de naissance', 
    					validators=[DataRequired(), Length(min=2, max=20)], render_kw={"placeholder": "Casablanca"}) 
    
    submit = SubmitField('Enregistrer')