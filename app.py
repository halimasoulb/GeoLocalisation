from datetime import datetime
import enum, json
from threading import Condition

from flask import Flask, render_template, url_for, flash, redirect, request, Blueprint, g, make_response
from forms import RegistrationForm, LoginForm, RegisterForm
from forms import ChangeStatus

from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin, LoginManager, current_user, login_required, login_user, logout_user
from flask_googlemaps import GoogleMaps, Map, icons
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, DateTime, JSON, Enum, create_engine
from sqlalchemy.orm import sessionmaker
from models import Case, User


Base = declarative_base()

class Covid19Monitor(object):
    def __init__(self):
        self.cv = Condition()
        self.app = Flask(__name__)
        self.app.config['GOOGLEMAPS_KEY'] = "AIzaSyDcA0xJAaREE2vCdgjDnE-j9HQDChCvmWg"
        GoogleMaps(self.app)
        self.login_manager = LoginManager(self.app)
        #engine = create_engine('postgres://btdopsdlodkkkc:f2831c4692e5f0eedaa5769a343800697f23b11c339ee02629a13b8eff2e3503@ec2-3-218-123-191.compute-1.amazonaws.com:5432/dd9eehcgrnmn9m', echo=False)
        engine = create_engine('sqlite:///cas.db')
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()
        
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
            if form.validate():
                user = self.session.query(User).filter_by(email=form.email.data).first()
                if user is not None and user.verify_password(form.password.data):
                    login_user(user)
                    redirect(url_for('home'))
                    flash(f"Le fonctionnaire est connecte", "success")
                    return redirect(url_for('home'))
            return render_template('login.html', form=form)

        @app.route('/logout')
        def logout():
            logout_user()
            return redirect(url_for('home'))

      

        @app.route('/adduser', methods=["GET", "POST"])
        def adduser():
            form = RegisterForm()
            if form.validate():
                new_user = User(email=form.email.data, password=form.password.data)
                self.session.add(new_user)
                self.session.commit()
                self.session.close()
                redirect(url_for('login'))
                flash(f'Un nouveau utilisateur est enregistre', 'success')
                return redirect(url_for('login'))
            return render_template('adduser.html', form=form)

        @app.route('/selectform', methods=['GET'])
        def select():
            form = RegistrationForm()   
            return render_template_string(template, form=form)

        @app.route('/selectform', methods=['POST'])
        def updateselect():
            #aal = type(request.form.get('pachalik'))
            with open('config.js') as json_file:
                data = json.loads(json_file.read()) 
                liste = [(d, d["name"]) for d in data["liste"]]
                for d in data["liste"]:
                    choices = [{field : liste[i][field] for field in ['name']} \
                    for i in ["aal"] if i in liste]
                    response = make_response(json.dumps(choices))
                    response.content_type = 'application/jsons'
            return response

        @app.route("/register", methods=['GET', 'POST'])
        def register():
            form = RegistrationForm()
            if request.method == "POST" and form.validate():
                cases = self.session.query(Case).filter_by(cin=form.cin.data).all()
                if len(cases) > 1:
                    flash(u'Le patient portant ce cin existe deja', 'error')
                    return redirect(url_for('home'))
                else:
                    prenom = form.prenom.data
                    nom = form.nom.data
                    cin = form.cin.data
                    date = form.date.data
                    sexe = form.sexe.data
                    today = datetime.date.today()
                    date_de_naissance = form.date_de_naissance.data
                    age  = today.year - date_de_naissance.year - ((today.month, today.day) < (date_de_naissance.month, date_de_naissance.day))
                    adresse = form.adresse.data
                    residance = form.residance.data
                    employe = form.employe.data
                    id_societe = form.id_societe.data
                    nom_societe = form.nom_societe.data
                    observation = form.observation.data
                    pachalik = form.pachalik.data
                    aal = form.aal.data
                    cas = Case(nom=nom, prenom=prenom,cin=cin, type=Case.Type.NEW.value, position=position, date_de_naissance=date_de_naissance, 
                        age=age, date=date, sexe=sexe, adresse=adresse, residance=residance, employe=employe, id_societe=id_societe, nom_societe=nom_societe, observation=observation, pachalik=pachalik, aal=aal)
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
                    flash(u"Le patient avec cin = "+form.cin.data+" n'est pas enregistre", "error")
                elif len(cases) == 1:
                    self.session.query(Case).filter(Case.cin == form.cin.data).update({Case.type: form.status.data}, synchronize_session=False)
                    self.session.commit()
                    redirect(url_for('home'))
                    flash(f"L'etat du malade " + cases[0].nom + " " + cases[0].prenom + " a ete modifie", "success")
                    return redirect(url_for('home'))
                else:
                    flash(u"Le patient avec cin = "+form.cin.data+" est enregistre " +str(len(cases)) + " fois", "error")


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

