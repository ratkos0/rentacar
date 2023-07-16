#UVOZ PAKETA
from flask import Flask, render_template, url_for, session, redirect, flash, request, Response
from flask_mysqldb import MySQL
import yaml
from passlib.hash import sha256_crypt
#-------------------------------

#BOOTSTRAP i APP FLASK
from flask_bootstrap import Bootstrap
app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = 'Ratkos00!!'
#-------------------------------

#FLASK WTF FORME
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, PasswordField, FloatField
from wtforms.validators import DataRequired, Length
#-----------------------

#KONFIG MYSQLA
db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']
mysql = MySQL(app)
#--------------------------

class LoginForm(FlaskForm):
    username = StringField('Unesite Vase korisnicko ime', validators=[DataRequired()])
    password = PasswordField('Lozinka', validators=[DataRequired(), Length(min=8)])
    submit = SubmitField('Potvrdi')

class Register(FlaskForm):
    idKupca = IntegerField('Unesite Vas jedinstveni ID', validators=[DataRequired()])
    name = StringField('Unesite Vase ime.', validators=[DataRequired()])
    surname = StringField('Unesite Vase prezime.', validators=[DataRequired()])
    email = StringField('Unesite vasu email adresu', validators=[DataRequired()])
    Broj_telefona = IntegerField('Unesite vas broj telefon', validators=[DataRequired()])
    username = StringField('Unesite Vas username', validators=[DataRequired()])
    password = PasswordField('Lozinka', validators=[DataRequired(), Length(min=8)])
    verify_pass = PasswordField('Ponovo unesite lozinku', validators=[DataRequired(), Length(min=8)])
    submit = SubmitField('REGISTRACIJA')

class AddCar(FlaskForm):
    car_chassis = StringField('Unesite broj šasije:', validators=[DataRequired(), Length(min=17, max=17)])
    car_name = StringField('Unesite marku vozila:', validators=[DataRequired()])
    car_model = StringField('Unesite model vozila:', validators=[DataRequired()])
    car_year = IntegerField('Unesite godinu proizvodnje:', validators=[DataRequired()])
    car_engine = FloatField('Unesite litražu motora:', validators=[DataRequired()])
    car_kw = IntegerField('Koliko kilovata ima motor vozila:', validators=[DataRequired()])
    car_hp = IntegerField('Koliko konjskih snaga ima auto:', validators=[DataRequired()])
    car_price_a_day = IntegerField('Cijena vozila po danu:', validators=[DataRequired()])
    submit = SubmitField('Dodaj')

class RentaSetup(FlaskForm):
    comp_name = StringField('Naziv firme:', validators=[DataRequired()])
    comp_adress = StringField('Unesite adresu:', validators=[DataRequired()])
    comp_email = StringField('Unesite email adresu:', validators=[DataRequired()])
    comp_number = IntegerField('Broj telefona:', validators=[DataRequired()])
    submit = SubmitField('Potvrdi!')
    #comp = company

class Rezer(FlaskForm):
    days = IntegerField('Koliko dana želite iznajmiti vozilo:', validators=[DataRequired()])
    broj_sasije = IntegerField('Unesite broj sasije:', validators=[DataRequired(), Length(min=17, max=17)])
    submit = SubmitField('Potvrdi')


@app.route('/')
def index():
    if session.get('username') == None:
        flash('Niste prijavljeni.')
        return render_template('index.html')
    return render_template('index.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(e):
    return render_template('500.html'), 500

@app.route('/register/', methods=['GET', 'POST'])
def register():
    form = Register()
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        idKupca = request.form.get('idKupca')
        name = request.form.get('name')
        surname = request.form.get('surname')
        email = request.form.get('email')
        Broj_telefona = request.form.get('Broj_telefona')
        username = request.form.get('username')
        password = request.form.get('password')
        verify_pass = request.form.get('verify_pass')
        if password == verify_pass:
            if (cur.execute('SELECT * FROM Kupci WHERE email = %s', [email]) ==0):
                if (cur.execute('SELECT * FROM Kupci WHERE username = %s', [username]) ==0):
                    cur.execute('INSERT INTO Kupci(idKupci, Ime, Prezime, Email, Broj_telefona, username, password) VALUES (%s, %s, %s, %s, %s, %s, %s)', [idKupca ,name, surname, email, Broj_telefona, username, sha256_crypt.hash(password)])
                    mysql.connection.commit()
                    cur.close()
                    flash('Registration success, please log in', 'success')
                    return redirect('/login/')
                else:
                    flash('Username must be unique.', 'danger')
                    return render_template('register.html', form=form)
            else:
                flash('Email error.', 'danger')
                return render_template('register.html', form=form)
        else:
            flash("Passwords don't match.", 'danger')
            return render_template('register.html', form=form)
    return render_template('register.html', form=form)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if session.get('username') is None:
            cur = mysql.connection.cursor()
            username = request.form.get('username')
            pswrd = request.form.get('password')
            #Lenght is set to minimum 8 characters
            if (cur.execute('SELECT * FROM Kupci WHERE username = %s', [username])) != 0:
                try:
                    cur.execute('SELECT password FROM Kupci where username=%s', [username])
                    password = cur.fetchone()
                    if sha256_crypt.verify(pswrd , *password) == True:
                        session['login'] = True
                        session['username'] = request.form.get('username')
                        cur.execute('SELECT * FROM Kupci WHERE username = %s', [username])
                        data = cur.fetchone()
                        session['UserID'] = data[0]
                        session['FirstName'] = data[1]
                        session['LastName'] = data[2]
                        session['Email'] = data[3]
                        return redirect('/')
                    else:
                        flash('Password error', 'danger')
                        return render_template('login.html', form=form)
                except Exception as e:
                    flash(e)
                    return render_template('login.html', form=form)
            else:
                flash('Username not found.', 'danger')
                return render_template('login.html', form=form)
    return render_template('login.html', form=form)
   
    
@app.route('/cars/', methods=['GET', 'POST'])
def cars():
    username = session.get('username')
    cur = mysql.connection.cursor()
    form = AddCar()
    if username != None:
        cur.execute('SELECT Naziv FROM rent_a_car')
        name = cur.fetchone()
        car_chassis = request.form.get('car_chassis')
        car_name = request.form.get('car_name')
        car_model = request.form.get('car_model')
        car_year = request.form.get('car_year')
        car_engine = request.form.get('car_engine')
        car_kw = request.form.get('car_kw')
        car_hp = request.form.get('car_hp')
        car_price_a_day = request.form.get('car_price_a_day')
        if request.method == 'POST':
            if(cur.execute('SELECT Broj_sasije FROM Auta WHERE Broj_sasije=%s', [car_chassis])) == 0:
                try:
                    cur.execute('INSERT INTO Auta(Rent_a_car_Naziv, Broj_sasije, Marka, Model, Godina_proizvodnje, Motor, kW, hp, Cijena) VALUES (%s,%s, %s, %s, %s, %s, %s, %s, %s)', [*name,car_chassis,car_name, car_model, car_year, car_engine, car_kw, car_hp, car_price_a_day])
                    mysql.connection.commit()
                    cur.close()     
                    flash('Success', 'succcess')
                    return render_template('auta.html', form=form)
                except Exception as e:
                    flash('Da li ste podesili Vlasničke podatke kompanije?', 'danger')
                    #flash(e)
            else:
                flash('Broj šasije se nalazi u bazi, provjerite i pokušajte ponovo', 'danger')
                return render_template('auta.html', form=form)
        else:
            return render_template('auta.html', form=form)
    else:
        flash('Owner can add cars only.', 'info')
        return render_template('index.html')
        
        

@app.route('/listing/', methods=['GET', 'POST'])
def listing():
    cur = mysql.connect.cursor()
    data = cur.execute('SELECT * FROM Auta')
    if data > 0:    
        listing = cur.fetchall()
        return render_template('list-car.html', listing=listing)
    return render_template('list-car.html')


@app.route('/logout/', methods=['GET', 'POST'])
def logout():
    if session['login'] == True:
        session.pop('username', default=None)
        session.pop('FirstName', default=None)
        session.pop('LastName', default=None)
        session.pop('Email', default=None)
        session.pop('login',  default=False)
        #flash('Logged out!', 'success')
        return redirect('/')
    else:
        flash('No one is logged in', 'info')
        return render_template('index.html')


@app.route('/owner-setup/', methods=['GET', 'POST'])
def setup():
    form = RentaSetup()
    if request.method == 'POST':
        name = request.form.get('comp_name')
        adress = request.form.get('comp_adress')
        email = request.form.get('comp_email')
        number = request.form.get('comp_number')
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO rent_a_car(Naziv, Adresa, Email, Broj_telefona) VALUES(%s, %s, %s ,%s)', [name, adress, email, number])
        mysql.connection.commit()
        cur.close()
        flash('Success', 'success')
        return redirect('/')
    return render_template('renta-setup.html', form=form)


@app.route('/rezervacija/', methods=['GET', 'POST'])
def rezervacija():
    form = Rezer()
    flash(session.get('Email'))
    if request.method == 'POST':
        if session['login'] == False:
            flash('Ooops no login detected, please Log In and try again', 'danger')
            return render_template('login.html')
        else:
            try:
                cur = mysql.connection.cursor()
                sasija = request.form.get('broj_sasije')
                dani = request.form.get('days')
                cur.execute('SELECT Naziv FROM rent_a_car')
                name = cur.fetchone()
                cur.execute('INSERT INTO rezervacija(Kupci_idKupci ,Auta_Rent_a_car_Naziv, Auta_Broj_sasije, Dana) VALUES(%s, %s, %s, %s)', [session['UserID'], *name ,sasija, dani])
                mysql.connection.commit()
                cur.close()
                flash('Success', 'success')
            except Exception as e:
                flash(e)
    return render_template('rezervacija.html', form=form)
