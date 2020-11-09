from flask import Flask, render_template, url_for, flash, redirect, request
from forms import RegistrationForm
from dbconnect import connection
from pymysql import escape_string as thwart
import json


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
        prenom = form.prenom.data
        nom = form.nom.data
        age = form.age.data
        lieu_de_naissance = form.lieu_de_naissance.data
        c,conn = connection()
        c.execute("INSERT INTO  patients (prenom, nom, age, lieu_de_naissance) VALUES (%s, %s, %s, %s)",
                (thwart(prenom), thwart(nom), thwart(age), thwart(lieu_de_naissance)))

        conn.commit()
        flash("Cas enregistre")
        c.close()
        conn.close()
        return redirect(url_for('home'))
        
    return render_template('register.html', title='Register', form=form)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

