from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.mutable import MutableDict
from dbconnect import db
from datetime import datetime




class cas(db.Model):

  __tablename__ = 'cas'

  id = db.Column('id', db.Integer, primary_key = True) 
  prenom= db.Column(db.String(50), nullable=False)
  nom = db.Column(db.String(50), nullable=False)  
  date_de_naissance = db.Column(db.DateTime)
  lieu_de_naissance = db.Column(db.String(100), nullable=False)
  cin = db.Column(db.String(10), nullable=False)
  date_enregistrement = db.Column(db.DateTime)
  position = db.Column(db.JSON())

  def __init__(self, prenom, nom, date_de_naissance, lieu_de_naissance, cin, date_enregistrement, position):

    self.prenom = prenom
    self.nom = nom
    self.date_de_naissance = date_de_naissance
    self.lieu_de_naissance = lieu_de_naissance
    self.cin = cin
    self.date_enregistrement = date_enregistrement
    self.position = position

  def __repr__(self):
    return '<Register %r>' % self.prenom

