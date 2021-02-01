from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, DateTime, JSON, Enum, create_engine, Date, Table
import enum, json
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin, LoginManager, current_user, login_required, login_user, logout_user

Base = declarative_base()


class Case(Base):
    __tablename__ = 'Covid19Cases'

    class Type(enum.Enum):
        NEW = "Confirme"
        RECOVERED = "Gueri"
        DEAD = "Decede"
        HOSPITILIZED = "Hospitalise"
        LOADING = "En cours"
        CONFINED = "Confine"

    id = Column('id', Integer, primary_key = True) 
    nom = Column(String(50))  
    prenom= Column(String(50))
    cin = Column(String(10))
    age =  Column(String(10))
    type = Column(String(50))
    #position = Column(JSON())
    date_de_declaration = Column(String(50))
    sexe = Column(String(50))
    adresse = Column(String(100))
    residance = Column(String(50))
    employe = Column(String(50))
    id_societe = Column(String(50))
    nom_societe = Column(String(50))
    observation = Column(String(300))
    pachalik = Column(String(100))
    aal = Column(String(100))
    x = Column(String(10))
    y = Column(String(10))
    date_guerison = Column(String(50))
    date_hospitalisation = Column(String(50))
    lieu_hospitalisation = Column(String(100))
    date_deces = Column(String(50))

    def __repr__(self):
        return "<Case(nom='%s', prenom='%s', cin='%s', type='%s', age='%s', date_de_declaration='%s', sexe='%s', adresse='%s', residance='%s', employe='%s', id_societe='%s', nom_societe='%s', observation='%s', pachalik='%s', aal='%s', x='%s', y='%s', date_guerison='%s', date_hospitalisation='%s', lieu_hospitalisation='%s', date_deces='%s' )>" % (
            self.nom, self.prenom, self.cin, self.type, self.age, self.date_de_declaration, self.sexe, self.adresse, self.residance, self.employe, self.id_societe, self.nom_societe, self.observation, self.pachalik, self.aal, self.x, self.y, self.date_guerison, self.date_hospitalisation, self.lieu_hospitalisation, self.date_deces)

class User(Base, UserMixin):

    __tablename__ = 'user'

    id = Column('id', Integer, primary_key = True)
    email = Column(String(50), unique=True, index=True)
    password_hash = Column(String(128))

    def __repr__(self):
        return "<User(email='%s', password_hash='%s')>" % (self.email, self.password_hash)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


class Pachalik(Base):
    __tablename__ = 'Pachalik'

    id = Column('id', Integer, primary_key = True) 
    name = Column(String(50)) 

class Aal(Base):
    __tablename__ = 'Aal'

    id = Column('id', Integer, primary_key = True) 
    name = Column(String(50))
    pachalik_id =  Column(Integer) 





engine = create_engine('sqlite:///../cas.db')
Base.metadata.create_all(engine)


