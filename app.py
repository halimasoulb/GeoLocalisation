from flask import Flask, render_template, url_for, flash, redirect, request
from forms import RegistrationForm
from dbconnect import connection
from pymysql import escape_string as thwart
from datetime import datetime
import json
import requests
import demjson


app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'


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
        position = json.dumps(request.get_json())
        print(position)
        c,conn = connection()
        c.execute("INSERT INTO  register (prenom, nom, date_de_naissance, lieu_de_naissance, cin, date_enregistrement, position) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (thwart(prenom), thwart(nom), thwart(date_de_naissance), thwart(lieu_de_naissance), thwart(cin), thwart(date_enregistrement), thwart(position)))

        conn.commit()
        flash("Cas enregistre")
        c.close()
        conn.close()
        return redirect(url_for('home'))
        
    return render_template('register.html', title='Register', form=form)

if __name__ == '__main__':
    app.run(debug=True)

