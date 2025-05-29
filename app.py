from flask import Flask, render_template, redirect, url_for
from models.models import db, Transaction, Category
from forms import TransactionForm, CategoryForm
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
    # Dodajemy początkowe kategorie tylko jeśli brak
  


# Strona główna – lista transakcji
@app.route('/')
def home():
    transactions = Transaction.query.order_by(Transaction.date.desc()).all()
    return render_template('index.html', transactions=transactions)


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


# Dodawanie kategorii
@app.route('/add-category', methods=['GET', 'POST'])
def add_category():
    form = CategoryForm()
    if form.validate_on_submit():
        new_category = Category(name=form.name.data)
        db.session.add(new_category)
        db.session.commit()
        return redirect(url_for('list_categories'))
    return render_template('add_category.html', form=form)

# Edytowanie Kategorii
@app.route('/edit-category/<int:id>', methods=['GET', 'POST'])
def edit_category(id):
    category = Category.query.get_or_404(id)
    form = CategoryForm(obj=category)  # wypełni formularz danymi z category

    if form.validate_on_submit():
        category.name = form.name.data
        db.session.commit()
        return redirect(url_for('list_categories'))

    return render_template('edit_category.html', form=form)

# Usuwanie Kategorii 
@app.route('/delete-category/<int:id>', methods=['POST'])
def delete_category(id):
    category = Category.query.get_or_404(id)
    db.session.delete(category)
    db.session.commit()
    return redirect(url_for('list_categories'))
# LIsta Kategorii
@app.route('/categories')
def list_categories():
    categories = Category.query.all()
    return render_template('categories.html', categories=categories)

@app.route('/edit-transaction/<int:id>', methods=['GET', 'POST'])
def edit_transaction(id):
    transaction = Transaction.query.get_or_404(id)
    form = TransactionForm(obj=transaction)
    form.category.choices = [(c.id, c.name) for c in Category.query.all()]

    if form.validate_on_submit():
        transaction.amount = form.amount.data
        transaction.description = form.description.data
        transaction.category_id = form.category.data
        transaction.is_income = form.is_income.data
        transaction.date = form.date.data
        db.session.commit()
        return redirect(url_for('home'))

    return render_template('edit_transaction.html', form=form)

@app.route('/delete-transaction/<int:id>', methods=['POST'])
def delete_transaction(id):
    transaction = Transaction.query.get_or_404(id)
    db.session.delete(transaction)
    db.session.commit()
    return redirect(url_for('home'))


# Wykresy
@app.route('/charts')
def charts():
    from sqlalchemy import func
    # suma wydatków wg kategorii
    expense_data = db.session.query(
        Category.name,
        func.sum(Transaction.amount)
    ).join(Transaction).filter(Transaction.is_income == False).group_by(Category.name).all()

    # suma dochodów i wydatków
    income_sum = db.session.query(func.sum(Transaction.amount)).filter(Transaction.is_income == True).scalar() or 0
    expense_sum = db.session.query(func.sum(Transaction.amount)).filter(Transaction.is_income == False).scalar() or 0

    return render_template('charts.html', expense_data=expense_data, income_sum=income_sum, expense_sum=expense_sum)


# Uruchamianie aplikacji
if __name__ == '__main__':
    app.run(debug=True)
