from flask import Flask
from models.models import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/budget.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/')
def home():
    return "Hello, Budget Manager!"

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
from flask import render_template, redirect, url_for
from forms import TransactionForm
from models.models import Transaction, Category

app.config['SECRET_KEY'] = 'tajnyklucz'

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
