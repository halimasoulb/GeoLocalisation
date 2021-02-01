from datetime import datetime
import enum, json
from threading import Condition

from flask import Flask, render_template, url_for, flash, redirect, request, Blueprint, g, make_response,  jsonify 
from forms import RegistrationForm, LoginForm
from forms import ChangeStatus
import geocoder
from geopy.geocoders import Nominatim

from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin, LoginManager, current_user, login_required, login_user, logout_user
from flask_googlemaps import GoogleMaps, Map, icons
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, DateTime, JSON, Enum, create_engine
from sqlalchemy.orm import sessionmaker
import datetime

from configparser import ConfigParser


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



class Covid19Monitor(object):

    def __init__(self):
        self.cv = Condition()
        self.app = Flask(__name__)
        self.app.config['GOOGLEMAPS_KEY'] = "AIzaSyDcA0xJAaREE2vCdgjDnE-j9HQDChCvmWg"
        GoogleMaps(self.app)
        self.geolocator = Nominatim(user_agent="example app")
        self.login_manager = LoginManager(self.app)
        #engine = create_engine('postgres://btdopsdlodkkkc:f2831c4692e5f0eedaa5769a343800697f23b11c339ee02629a13b8eff2e3503@ec2-3-218-123-191.compute-1.amazonaws.com:5432/dd9eehcgrnmn9m', echo=False)
        engine = create_engine('sqlite:///cas.db')
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()
        #config = ConfigParser()
        #config.read('config.ini')
        #self.session = config['database']['Session']
        #self.app = config['flask']
        self.app.config['DEBUG'] = True
        self.app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
        self.position = {'latitude': 0, 'longitude': 0}
        self.locations = []


    def create(self, host=None, port=None, debug=None, load_dotenv=True, **options):
        app = self.app
        
        @app.before_request
        def before_request():
            g.user = current_user

        @self.login_manager.user_loader
        def load_user(user_id):
            return self.session.query(User).get(int(user_id))

        @app.route("/")
        @app.route("/home")
        def home():
            nbre_cas = self.session.query(Case).count()
            nbre_gueri = self.session.query(Case).filter_by(type=Case.Type.RECOVERED.value).count()
            nbre_mort = self.session.query(Case).filter_by(type=Case.Type.DEAD.value).count()
            nbre_hosp = self.session.query(Case).filter_by(type=Case.Type.HOSPITILIZED.value).count()
            nbre_conf = self.session.query(Case).filter_by(type=Case.Type.CONFINED.value).count()
            return render_template('home.html', new=nbre_cas, recovered=nbre_gueri, dead=nbre_mort, hosp=nbre_hosp, conf=nbre_conf)

        @app.route('/login', methods=["GET", "POST"])
        def login():
            form = LoginForm()
            nbre_users = self.session.query(User).count()
            if nbre_users == 0:
                with open('users.js') as json_file:
                    users = json.loads(json_file.read())
                    all_users = []
                    for user in users:
                        new_entry = User(id=user["id"], email=user["email"], password=user["password"])
                        all_users.append(new_entry)
                    self.session.add_all(all_users)
                    self.session.commit()
            else:
                if form.validate():
                    user = self.session.query(User).filter_by(email=form.email.data).first()
                    if user is not None and user.verify_password(form.password.data):
                        login_user(user)
                        redirect(url_for('home'))
                        flash(f"Vous etes connecte", "success")
                        return redirect(url_for('home'))
                    else:
                        flash(f'Email ou mot de passe incorrect', 'success')
            return render_template('login.html', form=form)

        @app.route('/logout')
        def logout():
            logout_user()
            return redirect(url_for('home'))

        @app.route('/register')
        def getPachalik():
            form = RegistrationForm()
            nbre_pachaliks = self.session.query(Pachalik).count()
            nbre_aals = self.session.query(Aal).count()
            if nbre_pachaliks==0 and nbre_aals==0:
                with open('config.json') as json_file:
                    pachaliks = json.loads(json_file.read())
                    all_pachaliks = []
                    for pachalik in pachaliks:
                        if pachalik["parent_id"] == 0:
                            new_pachalik = Pachalik(id=pachalik["id"], name=pachalik["name"])
                            all_pachaliks.append(new_pachalik)   
                    self.session.add_all(all_pachaliks)
                with open('config.json') as json_file:
                    aals  = json.loads(json_file.read())
                    all_aals = []
                    for aal in aals:
                        if aal["parent_id"] > 0:
                            new_aal = Aal(name=aal["name"], pachalik_id=aal["parent_id"])
                            all_aals.append(new_aal)
                    self.session.add_all(all_aals)
                    self.session.commit()
            else:
                form.pachalik.choices = [(pachalik.id, pachalik.name) for pachalik in self.session.query(Pachalik).all()]

                if request.method == 'POST':
                    aal = self.session.query(Aal).filter_by(id=form.aal.data).first()
                    pachalik = self.session.query(Pachalik).filter_by(id=form.pachalik.data).first()
                    return '<h1>Pachalik : {}, Aal: {}</h1>'.format(pachalik.name, aal.name)

            return render_template('register.html', form=form)

        @app.route('/aal/<get_aal>')
        def aalbypachalik(get_aal):
            aals = self.session.query(Aal).filter_by(pachalik_id=get_aal).all()
            aalArray = []
            for aal in aals:
                aalObj = {}
                aalObj['id'] = aal.id
                aalObj['name'] = aal.name
                aalArray.append(aalObj)
                print(aalArray)
            return jsonify({'aalpachalik' : aalArray})

        
        @app.route("/register", methods=['GET', 'POST'])
        def register():
            form = RegistrationForm()
            if request.method == "POST" and form.validate():
                cases = self.session.query(Case).filter_by(cin=form.cin.data).all()
                if len(cases) >= 1:
                    flash(f'Le patient portant ce cin existe deja', 'success')
                    return redirect(url_for('home'))
                else:
                    prenom = form.prenom.data
                    nom = form.nom.data
                    cin = form.cin.data
                    date = form.date.data.strftime("%d/%m/%Y")
                    sexe = dict(form.sexe.choices).get(form.sexe.data)
                    today = datetime.date.today()
                    date_de_naissance = form.date_de_naissance.data
                    age  = today.year - date_de_naissance.year - ((today.month, today.day) < (date_de_naissance.month, date_de_naissance.day))
                    adresse = form.adresse.data
                    residance = dict(form.residance.choices).get(form.residance.data)
                    employe = dict(form.employe.choices).get(form.employe.data)
                    id_societe = form.id_societe.data
                    nom_societe = form.nom_societe.data
                    observation = form.observation.data
                    pachalik = dict(form.pachalik.choices).get(form.pachalik.data)
                    aal = dict(form.pachalik.choices).get(form.pachalik.data)
                    x = self.geolocator.geocode(adresse).point.latitude
                    y = self.geolocator.geocode(adresse).point.longitude
                    cas = Case(nom=nom, prenom=prenom,cin=cin, type=Case.Type.NEW.value,
                        age=age, date_de_declaration=date, sexe=sexe, adresse=adresse, residance=residance, employe=employe, id_societe=id_societe, nom_societe=nom_societe, observation=observation, pachalik=pachalik, aal=aal, x=x, y=y, date_guerison=None, date_hospitalisation=None, lieu_hospitalisation=None, date_deces=None)
                    self.session.add(cas)
                    self.session.commit()
                    self.session.close()
                    redirect(url_for('home'))
                    flash(f'Un nouveau cas est enregistre', 'success')
                    return redirect(url_for('home'))
            return render_template('register.html', title='Register', form=form)

        @app.route('/update', methods = ['GET','POST'])
        def update():
            form = ChangeStatus([Case.Type.RECOVERED.value, Case.Type.DEAD.value, Case.Type.HOSPITILIZED.value, Case.Type.LOADING.value, Case.Type.CONFINED.value ])
            if request.method == 'POST' and form.validate():
                cases = self.session.query(Case).filter_by(cin=form.cin.data).all()
                if len(cases) == 0:
                    flash(f"Le patient avec cin = "+form.cin.data+" n'est pas enregistre", "success")
                elif len(cases) == 1:
                    status = form.status.data
                    date_guerison = form.date_guerison.data
                    date_hospitalisation = form.date_hospitalisation.data
                    date_deces = form.date_deces.data
                    lieu_hospitalisation = form.lieu_hospitalisation.data
                    self.session.query(Case).filter(Case.cin == form.cin.data).update({Case.type: status, Case.date_guerison: date_guerison, Case.date_hospitalisation :date_hospitalisation, Case.date_deces:date_deces, Case.lieu_hospitalisation: lieu_hospitalisation }, synchronize_session=False)
                    self.session.commit()
                    redirect(url_for('home'))
                    flash(f"L'etat du malade " + cases[0].nom + " " + cases[0].prenom + " a ete modifie", "success")
                    return redirect(url_for('home'))
                else:
                    flash(f"Le patient avec cin = "+form.cin.data+" est enregistre " +str(len(cases)) + " fois", "success")

            return render_template('update.html', title='Update', form=form)

       

        @app.route('/position', methods = ['POST'])
        def position():
            if request.method == 'POST':
                self.position = request.get_json()
                print("\n Current Position {}\n".format(self.position))


            return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 

        @app.route("/monitor", methods=['GET', 'POST'])
        def monitor():
            locations = []
            cases = self.session.query(Case).all()
            print("---------------------------------------------------------------------------")
            print(cases)
            print("---------------------------------------------------------------------------")

            for case in cases:
                locations.append(case.position)

            gmap = Map(
                identifier="gmap",
                varname="gmap",
                lat=locations[0]['latitude'],
                lng=locations[0]['longitude'],
                markers=[(loc['latitude'], loc['longitude']) for loc in locations],
                fit_markers_to_bounds = False,
                style="height:720px;width:1280px;margin:auto;",
            )
            return render_template('map.html', gmap=gmap)


        return self.app


app = Covid19Monitor().create()

if __name__ == '__main__':
    app.run(host="0.0.0.0")

