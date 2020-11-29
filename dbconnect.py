from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.mutable import MutableDict
from app import Covid19Monitor



class register(db.Model):

   id = db.Column('id', db.Integer, primary_key = True) 
   prenom= db.Column(db.String(50), nullable=False)
   nom = db.Column(db.String(50), nullable=False)  
   date_de_naissance = db.Column(db.Date)
   lieu_de_naissance = db.Column(db.String(100), nullable=False)
   cin = db.Column(db.String(10), nullable=False)
   date_enregistrement = db.Column(db.Date)
   position = db.Column(db.JSONB)

   def __init__(self, prenom, nom, date_de_naissance, lieu_de_naissance, cin, date_enregistrement, position, db):

    self.db = SQLAlchemy(app)
    self.prenom = prenom
    self.nom = nom
    self.date_de_naissance = date_de_naissance
    self.lieu_de_naissance = lieu_de_naissance
    self.cin = cin
    self.date_enregistrement = date_enregistrement
    self.position = position
    return self.db