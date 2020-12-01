from datetime import datetime
import json
from threading import Condition

from flask import Flask, render_template, url_for, flash, redirect, request
from forms import RegistrationForm
#from dbconnect import connection
#from pymysql import escape_string as thwart
from modeldb import Cas
from flask_sqlalchemy import SQLAlchemy
#import sqlalchemy as db

from flask_googlemaps import GoogleMaps, Map, icons


class Covid19Monitor(object):
    def __init__(self):
        self.cv = Condition()
        self.app = Flask(__name__)
        self.app.config['GOOGLEMAPS_KEY'] = "AIzaSyDcA0xJAaREE2vCdgjDnE-j9HQDChCvmWg"
        GoogleMaps(self.app)
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://tygqsltanlysiq:68be0239d03e66b403a43f493822bb0d7b9b776be3d8c0399066436f7d77c6dd@ec2-3-210-23-22.compute-1.amazonaws.com:5432/d8rn5mpu5ua96b'
        self.db = SQLAlchemy(self.app)
        self.db.create_all()
        self.db.session.commit()
        self.app.config['DEBUG'] = True
        self.app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
        self.position = {'latitude': 0, 'longitude': 0}
        self.locations = [
            {
                'latitude': 31.630000,
                'longitude': -8.008889
            },
            {
                'latitude': 48.7667,
                'longitude': 1.9167
            }
        ]


    def create(self, host=None, port=None, debug=None, load_dotenv=True, **options):
        app = self.app

        @app.route("/")
        @app.route("/home")
        def home():
            return render_template('home.html')

        @app.route("/register", methods=['GET', 'POST'])
        def register():
            form = RegistrationForm()
            if request.method == "POST" and form.validate():
                date_enregistrement =  datetime.now()
                prenom = form.prenom.data
                nom = form.nom.data
                date = form.date.data
                lieu_de_naissance = form.lieu_de_naissance.data
                cin = form.cin.data
                position = json.dumps(self.position)
                #engine = db.create_engine('sqlite:///test.sqlite')
                #metadata = db.MetaData()
                #connection = engine.connect()
                #emp = db.Table('emp', metadata, autoload=True, autoload_with=engine)
                #self.db.create_all()
                cases = Cas(prenom, nom, date, lieu_de_naissance, cin, date_enregistrement, position)
                self.db.session.add(cases)
                self.db.session.commit()
                #c,conn = connection()
                #c.execute("INSERT INTO  register (prenom, nom, date_de_naissance, lieu_de_naissance, cin, date_enregistrement, position) VALUES (%s, %s, %s, %s, %s, %s, '"+position+"')",
                #        (thwart(prenom), thwart (nom), thwart(date_de_naissance), thwart(lieu_de_naissance), thwart(cin), thwart(date_enregistrement)))

                #conn.commit()
                redirect(url_for('home'))
                flash('Un nouveau cas est enregistre')
                self.db.session.close()

                #c.close()
                #conn.close()
                return redirect(url_for('home'))

            return render_template('register.html', title='Register', form=form)

        @app.route('/position', methods = ['POST'])
        def position():
            if request.method == 'POST':
                self.position = request.get_json()
                print("\n Current Position {}\n".format(self.position))


            return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 

        @app.route("/monitor", methods=['GET', 'POST'])
        def monitor():
            gmap = Map(
                identifier="gmap",
                varname="gmap",
                lat=self.locations[0]['latitude'],
                lng=self.locations[0]['longitude'],
                markers=[(loc['latitude'], loc['longitude']) for loc in self.locations],
                fit_markers_to_bounds = True,
                style="height:720px;width:1280px;margin:auto;",
            )
            return render_template('map.html', gmap=gmap)


        return self.app


app = Covid19Monitor().create()

if __name__ == '__main__':
    app.run(host="0.0.0.0")

