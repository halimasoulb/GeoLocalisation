from datetime import datetime
import enum, json
from threading import Condition

from flask import Flask, render_template, url_for, flash, redirect, request
from forms import RegistrationForm
from forms import ChangeStatus

from flask_googlemaps import GoogleMaps, Map, icons
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, DateTime, JSON, Enum, create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Case(Base):
    __tablename__ = 'Covid19Cases'

    class Type(enum.Enum):
        NEW = "Confirme"
        RECOVERED = "Gueri"
        DEAD = "Decede"

    id = Column('id', Integer, primary_key = True) 
    nom = Column(String(50))  
    prenom= Column(String(50))
    cin = Column(String(10))
    type = Column(String(50))
    position = Column(JSON())
    date = Column(DateTime)

    def __repr__(self):
        return "<Cas(nom='%s', prenom='%s', cin='%s', type='%s', position='%s' date='%s')>" % (
            self.nom, self.prenom, self.cin, self.type, self.position, self.date)


class Covid19Monitor(object):
    def __init__(self):
        self.cv = Condition()
        self.app = Flask(__name__)
        self.app.config['GOOGLEMAPS_KEY'] = "AIzaSyDcA0xJAaREE2vCdgjDnE-j9HQDChCvmWg"
        GoogleMaps(self.app)
        engine = create_engine('postgres://leyuerbdnpvfns:084836b16199ffa8454ba3736cf63795ab8309f5692a8f286c36ca93268aaad0@ec2-52-22-238-188.compute-1.amazonaws.com:5432/d7c42auhofkp0l', echo=False)
        #engine = create_engine('sqlite:///cas.db')
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()

        self.app.config['DEBUG'] = True
        self.app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
        self.position = {'latitude': 0, 'longitude': 0}
        self.locations = []


    def create(self, host=None, port=None, debug=None, load_dotenv=True, **options):
        app = self.app

        @app.route("/")
        @app.route("/home")
        def home():
            nbre_cas = self.session.query(Case).count()
            nbre_gueri = self.session.query(Case).filter_by(type=Case.Type.RECOVERED.value).count()
            nbre_mort = self.session.query(Case).filter_by(type=Case.Type.DEAD.value).count()
            return render_template('home.html', new=nbre_cas, recovered=nbre_gueri, dead=nbre_mort)

        @app.route("/register", methods=['GET', 'POST'])
        def register():
            form = RegistrationForm()
            if request.method == "POST" and form.validate():
                cases = self.session.query(Case).filter_by(cin=form.cin.data).all()
                if len(cases) > 1:
                    flash('Le patient portant ce cin existe deja')
                    return redirect(url_for('home'))
                else:
                    prenom = form.prenom.data
                    nom = form.nom.data
                    cin = form.cin.data
                    date = form.date.data
                    cas = Case(nom=nom, prenom=prenom, cin=cin, type=Case.Type.NEW.value, position=self.position, date=date)
                    self.session.add(cas)
                    self.session.commit()
                    self.session.close()
                    redirect(url_for('home'))
                    flash('Un nouveau cas est enregistre')
                    return redirect(url_for('home'))
            return render_template('register.html', title='Register', form=form)

        @app.route('/update', methods = ['GET','POST'])
        def update():
            form = ChangeStatus([Case.Type.RECOVERED.value, Case.Type.DEAD.value])
            if request.method == 'POST' and form.validate():
                cases = self.session.query(Case).filter_by(cin=form.cin.data).all()
                if len(cases) == 0:
                    flash("Le patient avec cin = "+form.cin.data+" n'est pas enregistre" )
                elif len(cases) == 1:
                    self.session.query(Case).filter(Case.cin == form.cin.data).update({Case.type: form.status.data}, synchronize_session=False)
                    self.session.commit()
                    redirect(url_for('home'))
                    flash("L'etat du malade " + cases[0].nom + " " + cases[0].prenom + " a ete modifie")
                    return redirect(url_for('home'))
                else:
                    flash("Le patient avec cin = "+form.cin.data+" est enregistre " +str(len(cases)) + " fois" )


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

