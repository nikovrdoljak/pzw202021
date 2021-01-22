# Predavanje 12: FlaskSQLAlchemy, Migracije, Autentikacija (flask-login)
Predavanje se nastavlja na predavanje 10 (u kojem smo se upoznali s SQLite bazom podataka i SQLAlchemy ekstenzijom), a pokazat ćemo kako povezati Flask view funkcije i forme s bazom podataka uz pomoć [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/) ekstenzije. U bazu podataka ćmo spremati korisnike, pregledavati ih, mijenjati i brisati.

U drugom dijelu predavanja pokazat ćemo rad s migracijskim skriptama za rad s bazom podataka. Koristit ćemo [Flask-Migrate](https://flask-migrate.readthedocs.io/) ekstenziju.

Ukupno treba proći 6 zadatka za kompletiranje predavanja.

## Zadatak 1 - pokrenuti projekt i dodati CSS temu
* Klonirati projekt, aktivirati virualnu okolinu, instalirati potrebne ekstenzije, podesiti potrebne Flask varijable, te pokrenuti projekt.
  * ```git clone http://www.... i pozicionirajte se u mapu "p12-..."```
  * ```py -m venv venv```
  * ```.\venv\Scripts\Activate.ps1```
  * ```pip install -r requirements.txt```
  * ```$env:FLASK_APP="app.py"```
  * ```$env:FLASK_DEBUG=1```
  * ```flask run```
* Pregledati strukturu i funkcionalnost projekta. Projekt koristi [Bootstrap 4](https://getbootstrap.com/) web framework.
* Dodati neku drugu temu. Na stranicama [Bootswatch](https://bootswatch.com/) pogledati koje postoje, a jednostavno se aktiviraju preko [flask-bootstrap ekstenzije](https://bootstrap-flask.readthedocs.io/en/stable/advanced.html#bootswatch-theme) dodavanje slijedećeg koda u ```app.py``` datoteku:
```
app.config['BOOTSTRAP_BOOTSWATCH_THEME'] = 'minty'
```

## Zadatak 2 - flask-sqlalchemy
U ovom zadatku ćemo ponoviti kako radimo s SQLAlchemy ekstenzijom za Flask.
* Instalirati flask-sqlalchemy:
```python
pip install flask-sqlalchemy
```
* U app.py datoteku dodati slijedeći kod, te ga proučite:
```python
import os
from flask_sqlalchemy import SQLAlchemy
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')
    def __repr__(self):
        return '<Role %r>' % self.name

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    def __repr__(self):
        return '<User %r>' % self.username

@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            db.session.commit()
            session['known'] = False
        else:
            session['known'] = True

        if old_name is not None and old_name != form.name.data:
            flash('Čini se da si promijenio ime!')
        
        session['name'] = form.name.data
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'),known=session.get('known', False))
```
* U index.html predložak promijenite u:
```html
<div class="page-header">
    <h1>Pozdrav {% if name %}{{ name }}{% else %}stranče{% endif %}!</h1>
    {% if not known %}
    <p>Drago mi je da smo se upoznali!</p>
    {% else %}
    <p>Drago mi je da ste se vratili!</p>
    {% endif %}
</div>
```
* Prije ponovnog pokretanja aplikacije pokrenite slijedeći kod u Flask konzoli kako biste kreirali SQLite bazu podataka, te ju pregledajte u programu "DB Browser (SQLite)":
```python
(venv) flask shell
>>> from app import db
>>> db.create_all()
```
* Pokrenite ponovo aplikaciju, te unesite jednog ili više korisnika. Pogledajte u bazi da li su korisnici upisani.
* Pokrenite aplikaciju u VS Code-u, postavite "breakpoint" na prvi red funkcije index(), te pratite u "Debug" prozoru korak po korak (F10) vrijednosti varijabli i izvođenje programa.

## Zadatak 3 - Pregled korisnika
* Dodajte dva nova predloška
    * "users.html" koji izlistava sve korisnike,
    * "user.html" koji ispisuje podatak o korisniku.
* Dodati u layout.html link na popis korisnika:
```html
<li><a class="nav-link" href="{{ url_for('users')}}">Korisnici</a></li>
```
* Dodati novi view s rutom:
```python
@app.route('/users')
def users():
    users = User.query.all()
    return render_template('users.html', users=users)
```
* Dodati u users.html predložak:
```
{% extends "layout.html" %}
{% block title %}Korisnici - {% endblock %}
{% block page_content %}
<div class="page-header">
    <h1>Korisnici</h1>
</div>
<div>
    <ul>
        {% for user in users %}
            <li>{{ user.username }}</li>            
        {% endfor %}
    </ul>
</div>
{% endblock %}
```
* Pokrenite aplikaciju i pogledajte da li su svi korisnici ispisani.
* Promijenite liniju s ispisom korisnika u link:
```html
<li><a href="{{ url_for('user', id=user.id )}}">{{ user.username }}</a></li>
```
* Dodati user view:
```python
@app.route('/user/<id>')
def user(id):
    user = User.query.get (id)
    return render_template('user.html', user=user)
```
* Dodati u user.html predložak:
```
{% extends "layout.html" %}
{% block title %}Korisnik | {{ user.username }} - {% endblock %}
{% block page_content %}
<div class="page-header">
    <h1>Korisnik: <b>{{ user.username }}</b></h1>
</div>
{% endblock %}
```
* Pokrenite aplikaciju i provjerite da se na klik korisnika otvara stranica s podacima o korisniku. Probajte u pregledniku direktno promijeniti _id_ parametar u neki drugi. Što se dešava ako upišete nepostojeći _id_?

## Zadatak 4 – dodati stranicu za grešku 404
Promijeniti get u get_or_404() i prikazati grešku, tj. dodati error404.html predložak s tekstom i funkciju:
* view funkcija:
```python
@app.errorhandler(404)
def page_not_found(e):
	return render_template('error404.html'), 404
```

* predložak _error404.html_:
```
{% extends "layout.html" %}
{% block title %}Nepostojeći sadržaj - {% endblock %}
{% block page_content %}
<div class="page-header">
    <h3 class="text-danger">Sadržaj koji tražite ne postoji</h3>
</div>
{% endblock %}
```

## Zadatak 5 – brisanje
* Dodati na "user.html" predložak link (botun) za brisanje:
```html
<a class="btn btn-danger" href="{{ url_for('userdelete', id=user.id ) }}" role="button">Briši</a>
```
* Dodati delete user view:
```python
@app.route('/userdelete/<id>')
def userdelete(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    flash('Korisnik uspješno pobrisan.')
    return redirect(url_for('users'))
```
# Migracije
## Zadatak 6 - migracije
* Instalirati flask-migrate:
```
pip install flask-migrate
```
* Dodajemo u app.py:
```python
from flask_migrate import Migrate
migrate = Migrate(app, db)
```
* Pokrenuti naredbu koja inicira migracije te stvara migrations folder sa svim potrebnim datotekama:
```
flask db init
```
* Promijenite naziv "data.sqlite" baze kako bismo stvorili novu (ili ju pobrišite)
* Kreiramo inicijalnu skriptu koja služi za stvaranje baze podataka:
```
flask db migrate -m "initial migration"
```
* Pregledajte stvorenu skriptu u "migrations/versions" mapi.
* Stvorena je i nova baza, ali je prazna, tj. u njoj se nalazi samo jedna, pomoćna tablica "_alembic_version_".
* Ažurirajmo novu bazu prema našem Python SQLAlchemy modelu pozivom naredbe:
```
flask db upgrade
```
* Pregledajte novostvorenu bazu
* Dodajte novo polje u User klasu. Npr. email. Ponovite naredbe:
```
flask db migrate -m "dodan email"
flask db upgrade
```
* Ponovo otvorite bazu i primijetit ćete novo polje. Također dodana je i nova migracijska skripta.

## Domaći rad
Napravite ažuriranje korisnika, brisanje s potvrdom, upravljanje rolama, dodavanje korisnika u rolu, dodajte novu tablicu i sl.


# Autentikacija

* Proces u kojem ustanovljavamo tko ili što jest ili se deklarira da je
* Odvija se na način da uspoređujemo vjerodajnice (credentials) korisnika sa vjerodajnicama spremljenim u bazi autentikacijskog poslužitelja
* Autentikacija je bitna jer omogućava da određenim resursima smiju pristupiti samo ovlašteni korisnici ili procesi 

## Faktori autentikacije
* **Faktor znanja** – ono što korisnik zna – zaporka, fraza, PIN, odgovor na pitanje
* **Faktor vlasništva** – ono što korisnik ima – kartica, narukvica, telefon…
* **Faktor pripadnosti** – ono što korisnik jest ili radi – otisak prsta, mrežnica, glas, lice, potpis…
* **Faktor vremena**
* **Faktor lokacije**

Da bi se osoba pozitivno autenticirala, poželjno je da elementi barem dva faktora budu verificirani.

## Tipovi autentikacije
* Single-factor
    * Provjera autentičnosti s jednim faktorom
    * Najslabija i nepoželjna za transakcije koje traže visok nivo zaštite
* Two-factor
    * Bankomat – nešto što korisnik ima (kartica) i zna (PIN)
    * Ili zaporka (znamo) + token (imamo; na uređaju)
* Multi-factor

## Autentikacija u flasku
* Korisnički ime ili email + zaporka
* Flask-login
    * Ekstenzija za upravljanje sesijama prijavljenih korisnika
    * ```pip install flask-login```
* Forma za prijavu
    * LoginForm
    * ```pip install flask-wtf``` (imamo od ranije u projektu)

## Zaštita zaporke
Zaporka se nikad ne smije spremati u izvornom obliku, te se sprema njen *hash*.
Hashing funkcija uzima zaporku kao ulazni argument, dodaje slučajnu sekvencu (*salt*) i primjenjuje jednosmjernu kriptografsku funkciju. Rezultat je sekvenca iz koje se ne može reverzno dobiti izvornu zaporku. Zatim uspoređujemo *hashiranu* zaporku koju je korisnik upisao s onom u bazi. Detaljnije o ovoj temi možete pronaći na linku: [Salted Password Hashing - Doing it Right](https://crackstation.net/hashing-security.htm)

### Zadatak 7
```python
flask shell
>>> from werkzeug.security import generate_password_hash, check_password_hash
>>> hash1 = generate_password_hash('123')
>>> print(hash1)
pbkdf2:sha256:50000$ClVWrTj0$d9ef0819c7bcd9ac996079d284f87f4969f3ba09e504c58a839a169ef10c7193
>>> check_password_hash(hash1, '123')
True
```

### Zadatak 8
Promijenimo User klasu da možemo dodati polje za spremanje hash-a zaporke. Nova klasa bi trebala izgledati ovako:
```python
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return '<User %r>' % self.username
```

Kreiramo skriptu i ažurirajmo novu bazu:
```
flask db migrate -m "added password"
flask db upgrade
```
Provjerimo kako to radi u _shellu_:
```python
flask shell
>>> from app import User
>>> u = User()
>>> u.password = '123'
>>> u.password
AttributeError: password is not a readable attribute
>>> u.password_hash
'pbkdf2:sha256:150000$4uay7o1E$1efe76f431c67bd69571a94e777b2a4931d138171fad305247e78114d2a735d8'
>>> u.verify_password('123')
True
```

### Zadatak 8
Dodat ćemo sad formu za logiranje te pripadnu programsku logiku uz pomoć [flask-login](https://flask-login.readthedocs.io/en/latest/) ekstenzije. Dodajmo najprije klasu za *login* formu u ```app.py```:
```python
class LoginForm(FlaskForm):
    email = TextField('E-mail', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('Zaporka', validators=[DataRequired()])
    remember_me = BooleanField('Ostani prijavljen')
    submit = SubmitField('Prijava')
```
te uvezimo dodatne potrebne module:
```python
from wtforms import TextField, PasswordField, BooleanField
from wtforms.validators import Length, Email
```
Email validator je potrebno zasebno instalirati:
```
pip install email-validator
```
Dodajmo rutu:
```python
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template('login.html', form=form)
```
i predložak ```login.html```
```
{% extends "layout.html" %}
{% from 'bootstrap/form.html' import render_form %}

{% block title %}Prijava - {% endblock %}

{% block page_content %}
    <div class="page-header">
        <h1>Prijava</h1>
    </div>
    <div class="col-md-4 mb-4">
        {{ render_form(form) }}
    </div>
{% endblock %}
```
U ```layout.html``` dodajmo link za prijavu (možemo maknuti polje za pretragu):
```html
    <ul class="nav navbar-nav navbar-right">
        <li><a class="nav-link" href="{{url_for('login')}}">Prijava</a></li>
    </ul>
```
Da bismo mogli jednostavnije raditi s prijavom, koristit ćemo [flask-login](https://flask-login.readthedocs.io/en/latest/) ekstenziju. Instalirajmo je:
```
pip install flask-login
```
Flask-login ekstenzija s brine o prijavi, odjavi i pamćenju korisnikove sesije tijekom vremena. Ona radi slijedeće:
* Pamti korisnički ID u sesiji i brine se o prijavi i odjavi
* Omogućava da označite koje *view-ove* može samo prijavljeni korisnik vidjeti
* Brine o implementaciji *"zapamti me"* funkcionalnosti
* Omogućava da netko ne može *ukrasti* korisničku sesiju
* Lako se integrira s drugim ekstenzijama poput *flask-principal* za autorizaciju

Ono što moramo sami napraviti je:
* Pobrinuti se gdje ćemo spremati podatke (u bazu npr.)
* Odlučiti koju metodu autentikacije ćemo koristiti (korisnik/zaporka, OpenID, i sl.)
* Brinuti o načinu registracije, obnovi zaporke i sl.

Dodajmo potrebne module:
```python
from flask_login import UserMixin
from flask_login import LoginManager, login_required, current_user, login_user, logout_user
```
Konfigurirajmo aplikaciju da koristi flask-login:
```python
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
```
I promijenimo ```User``` klasu da naslijeđuje i tzv. ```UserMixin``` klasu:
```python
class User(UserMixin, db.Model):
```

Dodajmo login rutu (za sad nećemo provjeravati zaporku):
```python
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None:
            login_user(user, form.remember_me.data)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('index')
            flash('Uspješno ste se prijavili!', category='success')
            return redirect(next)
        flash('Neispravno korisničko ime ili zaporka!', category='warning')
    return render_template('login.html', form=form)
```
Dodajmo i 
```python
from flask import request
```
Te na kraju dodajmo u ```index.html```:
```html
<div class="mt-4">
    <h4>current_user:</h4>
    <p>username: <b>{{current_user.username}}</b></p>
    <p>is_authenticated: <b>{{current_user.is_authenticated}}</b></p>
    <p>is_active: <b>{{current_user.is_active}}</b></p>
    <p>is_anonymous: <b>{{current_user.is_anonymous}}</b></p>
    <p>get_id(): <b>{{current_user.get_id()}}</b></p>
</div>
```
Te još jednu rutu, kojoj smije pristupiti samo autenticirani korisnik:
```python
@app.route('/secret')
@login_required
def secret():
    return "Ovu stranicu može vidjeti samo prijavljeni korisnil..."
```

### Zadatak 9
Dodajmo sad i fukcionalnost odjave. Promijenimo u ```layout.html``` link za prijavu:
```html
    <ul class="nav navbar-nav navbar-right">
        {% if current_user.is_authenticated %}
        <li><a href="{{url_for('logout')}}">Odjava</a></li>
        {% else %}
        <li><a href="{{url_for('login')}}">Prijava</a></li>
        {% endif %}
    </ul>
```
Dodajmo rutu za odjavu:
```python
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Odjavili ste se.', category='success')
    return redirect(url_for('index'))
```

### Zadatak 10
Sad ćemo dodati funkcionalnost registracije. Dodajmo rutu:
```python
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, username=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Sad se možete prijaviti', category='success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)
```
I dodajmo ```register.html``` predložak:
```
{% extends "layout.html" %}
{% from 'bootstrap/form.html' import render_form %}

{% block title %}Registracija - {% endblock %}

{% block page_content %}
    <div class="page-header">
        <h1>Registracija</h1>
    </div>
    <div class="col-md-4">
        {{ render_form(form) }}
    </div>
{% endblock %}
```
U ```login.html``` dodajmo gumb za registraciju ispod forme za prijavu:
```html
<div class="col-md-12" class="mt-4">
        Novi korisnik?<br> <a href="{{url_for('register')}}" class="btn btn-warning">Registrirajte se</a>
    </div>
```
Također u ```login``` ruti dodajmo da provjeravamo i valjanost zaporke:
```python
if user is not None and user.verify_password(form.password.data):
```
Registrirajmo novog korisnika, i prijavimo se s njim. Provjerimo kako u bazi izgleda novi zapis.

### Zadatak 11
Ovdje ćemo samo pokazati kako bi trebao izgledati proces potvrde registracije. Naime jedan od obaveznih koraka pri registraciji je potvrda iste mailom, gdje korisnik mora kliknuti aktivacijski link.
Taj link mora imati korsničko ime kriptirano, stoga moramo napraviti otprilike slijedeće:
```python
flask shell
>>> from itsdangerous import TimedJSONWebSignatureSerializer as serializer
>>> s = serializer(app.config['SECRET_KEY'], expires_in=3600)
>>> token = s.dumps({ 'potvrdi': 'nvrdoljak@unizd.hr' })
>>> token
b'eyJhbGciOiJIUzUxMiIsImlhdCI6MTU0MzkyMTE4NiwiZXhwIjoxNTQzOTI0Nzg2fQ.eyJwb3R2cmRpIjoibWFyaW9AdW5pemQuaHIifQ.tFRcBO0gjDzDcD4AL0eRx453ULdaq07MKWE6y-Nt8MnL3tesH7_VbFIFlcZSE2AxB1EdC3jbRdxSQ3o4JwDX_w'
>>> data = s.loads(token)
>>> data
{'potvrdi': 'nvrdoljak@unizd.hr'}
```
Sadržaj emaila može biti npr. ovakav:
```python
Poštovani {{ user.username }},
Da biste potvrdili svoju prijavu, molimo kliknite na slijedeći link:
{{ url_for('confirm', token=token, _external=True) }}
Srdačan pozdrav!
```
A pripadna ruta bi izgledala ovako:
```python
@app.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('index'))
    if current_user.confirm(token):
        db.session.commit()
        flash('Vaša prijava je potvrđena! Hvala.')
    else:
        flash('Link za potvrdu je neispravan ili je istekao.')
    return redirect(url_for('index'))
```

## Ostali scenariji
* Promjena passworda
* Resetiranje passworda
* Promjena email adrese

## Slijedeće
Autorizacija i korištenje ```flask-principal``` ekstenzije.
