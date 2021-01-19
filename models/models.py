from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, DateTime, JSON, Enum, create_engine, Date
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
    date_de_naissance = Column(Date)
    age =  Column(String(10))
    type = Column(String(50))
    position = Column(JSON())
    date = Column(DateTime)
    sexe = Column(String(50))
    adresse = Column(String(100))
    residance = Column(String(50))
    employe = Column(String(50))
    id_societe = Column(String(50))
    nom_societe = Column(String(50))
    observation = Column(String(300))
    pachalik = Column(String(100))
    aal = Column(String(100))

    def __repr__(self):
        return "<Case(nom='%s', prenom='%s', cin='%s', type='%s', position='%s', date_de_naissance='%s', age='%s', date='%s', sexe='%s', adresse='%s', residance='%s', employe='%s', id_societe='%s', nom_societe='%s', observation='%s', pachalik='%s', aal='%s')>" % (
            self.nom, self.prenom, self.cin, self.type, self.position, self.date_de_naissance, self.age, self.date, self.sexe, self.adresse, self.residance, self.employe, self.id_societe, self.nom_societe, self.observation, self.pachalik, self.aal)

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


engine = create_engine('sqlite:///cas.db')
Base.metadata.create_all(engine)


