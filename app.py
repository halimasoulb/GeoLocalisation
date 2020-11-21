from flask import Flask, render_template, url_for, flash, redirect, request
from forms import RegistrationForm
from dbconnect import connection
from pymysql import escape_string as thwart
from datetime import datetime
import json
import requests
from threading import Condition

class Covid19Monitor():
    def __init__(self):
        self.cv = Condition()
        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
        self.position = {'latitude': 0, 'longitude': 0}

    def start(self):
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
                c,conn = connection()
                c.execute("INSERT INTO  register (prenom, nom, date_de_naissance, lieu_de_naissance, cin, date_enregistrement, position) VALUES (%s, %s, %s, %s, %s, %s, '"+position+"')",
                        (thwart(prenom), thwart(nom), thwart(date_de_naissance), thwart(lieu_de_naissance), thwart(cin), thwart(date_enregistrement)))

                conn.commit()
                redirect(url_for('home'))
                flash("Cas enregistre")
                c.close()
                conn.close()
                return redirect(url_for('home'))

            return render_template('register.html', title='Register', form=form)

        @app.route('/position', methods = ['POST'])
        def position():
            if request.method == 'POST':
                self.position = request.get_json()
                print("\n Current Position {}\n".format(self.position))


            return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 

        self.app.run(host='0.0.0.0', threaded=True)



if __name__ == '__main__':
    covid19Monitor = Covid19Monitor()
    covid19Monitor.start()

