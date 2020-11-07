from flask import Flask, render_template, url_for, flash, redirect, request

from forms import RegistrationForm
from dbconnect import connection
from pymysql import escape_string as thwart


app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

posts = [
    {
        'author': 'Corey Schafer',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018'
    }
]


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


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
        flash("Cas enregiste")
        c.close()
        conn.close()
        return redirect(url_for('home'))
        
    return render_template('register.html', title='Register', form=form)

if __name__ == '__main__':
    app.run(debug=True)
