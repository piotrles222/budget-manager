from flask import Flask, render_template, redirect, url_for
from models.models import db, Transaction, Category
from forms import TransactionForm
import os

# Tworzenie aplikacji
app = Flask(__name__)

# Ścieżka absolutna do katalogu głównego projektu
basedir = os.path.abspath(os.path.dirname(__file__))

# Konfiguracja bazy danych
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data', 'budget.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'tajnyklucz'

# Inicjalizacja bazy danych
db.init_app(app)

# Tworzenie bazy danych przy pierwszym uruchomieniu
with app.app_context():
    if not os.path.exists(os.path.join(basedir, 'data')):
        os.makedirs(os.path.join(basedir, 'data'))
    db.create_all()

# Strona główna
@app.route('/')
def home():
    return "Hello, Budget Manager!"

# Dodawanie transakcji
@app.route('/add', methods=['GET', 'POST'])
def add_transaction():
    form = TransactionForm()
    form.category.choices = [(c.id, c.name) for c in Category.query.all()]
    if form.validate_on_submit():
        transaction = Transaction(
            amount=form.amount.data,
            description=form.description.data,
            is_income=form.is_income.data,
            category_id=form.category.data
        )
        db.session.add(transaction)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add_transaction.html', form=form)

# Uruchamianie aplikacji
if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, render_template, redirect, url_for
from models.models import db, Transaction, Category
from forms import TransactionForm
import os

# Tworzenie aplikacji
app = Flask(__name__)

# Ścieżka absolutna do katalogu głównego projektu
basedir = os.path.abspath(os.path.dirname(__file__))

# Konfiguracja bazy danych
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data', 'budget.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'tajnyklucz'

# Inicjalizacja bazy danych
db.init_app(app)

# Tworzenie bazy danych przy pierwszym uruchomieniu
with app.app_context():
    if not os.path.exists(os.path.join(basedir, 'data')):
        os.makedirs(os.path.join(basedir, 'data'))
    db.create_all()

# Strona główna
@app.route('/')
def home():
    return "Hello, Budget Manager!"

# Dodawanie transakcji
@app.route('/add', methods=['GET', 'POST'])
def add_transaction():
    form = TransactionForm()
    form.category.choices = [(c.id, c.name) for c in Category.query.all()]
    if form.validate_on_submit():
        transaction = Transaction(
            amount=form.amount.data,
            description=form.description.data,
            is_income=form.is_income.data,
            category_id=form.category.data
        )
        db.session.add(transaction)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add_transaction.html', form=form)

# Uruchamianie aplikacji
if __name__ == '__main__':
    app.run(debug=True)
