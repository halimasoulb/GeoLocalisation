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
    nom = Column(String(50), nullable=False)  
    prenom= Column(String(50), nullable=False)
    cin = Column(String(10), nullable=False)
    type = Column(Enum(Type))
    position = Column(JSON())
    date = Column(DateTime)

    def __repr__(self):
        return "<Cas(nom='%s', prenom='%s', cin='%s', type='%s', position='%s' date='%s')>" % (
            self.nom, self.prenom, self.cin, self.type.value, self.position, self.date)


class Covid19Monitor(object):
    def __init__(self):
        self.cv = Condition()
        self.app = Flask(__name__)
        self.app.config['GOOGLEMAPS_KEY'] = "AIzaSyDcA0xJAaREE2vCdgjDnE-j9HQDChCvmWg"
        GoogleMaps(self.app)
        engine = create_engine('postgres://tygqsltanlysiq:68be0239d03e66b403a43f493822bb0d7b9b776be3d8c0399066436f7d77c6dd@ec2-3-210-23-22.compute-1.amazonaws.com:5432/d8rn5mpu5ua96b', echo=False)
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
            return render_template('home.html', new=nbre_cas)

        @app.route("/register", methods=['GET', 'POST'])
        def register():
            form = RegistrationForm()
            if request.method == "POST" and form.validate():
                prenom = form.prenom.data
                nom = form.nom.data
                cin = form.cin.data
                date = form.date.data
                cas = Case(prenom=prenom, nom=nom, cin=cin, type=Case.Type.NEW, position=self.position, date=date)
                self.session.add(cas)
                self.session.commit()    
                redirect(url_for('home'))
                flash('Un nouveau cas est enregistre')
                return redirect(url_for('home'))

            return render_template('register.html', title='Register', form=form)

        @app.route('/update', methods = ['GET','POST'])
        def update():
            form = ChangeStatus([Case.Type.NEW.value, Case.Type.RECOVERED.value,Case.Type.DEAD.value])
            if request.method == 'POST' and form.validate():
                cases = self.session.query(Case).filter(case.cin == form.cin.data).all()
                if cases.count() > 1:
                    flash('La valeur du cin est dupplique')
                else:
                    self.session.query(Case).filter(cases.type == form[0]).update({cases.type: form.status.data}, synchronize_session = False)
                    self.session.commit()
                    redirect(url_for('home'))
                    flash('L etat du malade a ete modifie')
                    return redirect(url_for('home'))

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

