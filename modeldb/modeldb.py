from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.mutable import MutableDict
from datetime import datetime
import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, DateTime, JSON

Base = declarative_base()

class Cas(Base):

  __tablename__ = 'Cas'

  id = Column('id', Integer, primary_key = True) 
  prenom= Column(String(50), nullable=False)
  nom = Column(String(50), nullable=False)  
  date = Column(DateTime)
  lieu_de_naissance = Column(String(100), nullable=False)
  cin = Column(String(10), nullable=False)
  date_enregistrement = Column(DateTime)
  position = Column(JSON())

  def __init__(self, prenom, nom, date, lieu_de_naissance, cin, date_enregistrement, position):

    self.prenom = prenom
    self.nom = nom
    self.date = date
    self.lieu_de_naissance = lieu_de_naissance
    self.cin = cin
    self.date_enregistrement = date_enregistrement
    self.position = position

  def __repr__(self):
    return '<Register %r>' % self.prenom


