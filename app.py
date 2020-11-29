from datetime import datetime
import json
from threading import Condition

from flask import Flask, render_template, url_for, flash, redirect, request
from forms import RegistrationForm
#from dbconnect import connection
#from pymysql import escape_string as thwart

from flask_googlemaps import GoogleMaps, Map, icons


class Covid19Monitor(object):
    def __init__(self):
        self.cv = Condition()
        self.app = Flask(__name__)
        self.app.config['GOOGLEMAPS_KEY'] = "AIzaSyDcA0xJAaREE2vCdgjDnE-j9HQDChCvmWg"
        GoogleMaps(self.app)
        self.app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
        self.position = {'latitude': 0, 'longitude': 0}

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
                date_enregistrement =  datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                prenom = form.prenom.data
                nom = form.nom.data
                date_de_naissance = form.date_de_naissance.data.strftime('%Y-%m-%d %H:%M:%S')
                lieu_de_naissance = form.lieu_de_naissance.data
                cin = form.cin.data
                position = json.dumps(self.position)
                #c,conn = connection()
                #c.execute("INSERT INTO  register (prenom, nom, date_de_naissance, lieu_de_naissance, cin, date_enregistrement, position) VALUES (%s, %s, %s, %s, %s, %s, '"+position+"')",
                #        (thwart(prenom), thwart (nom), thwart(date_de_naissance), thwart(lieu_de_naissance), thwart(cin), thwart(date_enregistrement)))

                #conn.commit()
                #redirect(url_for('home'))
                #flash(f'Un nouveau cas est enregistre')
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
                lat=31.630000,
                lng=-8.008889,
                markers=
                    {
                        icons.dots.red: [(31.630000, -8.008889)]
                    },
                style="height:720px;width:1280px;margin:auto;",
            )
            return render_template('map.html', gmap=gmap)


        return self.app


app = Covid19Monitor().create()

if __name__ == '__main__':
    app.run()

