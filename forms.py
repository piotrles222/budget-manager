from flask_wtf import FlaskForm
from wtforms import DecimalField, StringField, SelectField, BooleanField, SubmitField, DateTimeField
from wtforms.validators import DataRequired
from datetime import datetime

class TransactionForm(FlaskForm):
    amount = DecimalField("Kwota", validators=[DataRequired()])
    description = StringField("Opis")
    is_income = BooleanField("Dochód?")
    category = SelectField("Kategoria", coerce=int)
    date = DateTimeField('Data', default=datetime.utcnow, format='%Y-%m-%d %H:%M')
    submit = SubmitField("Dodaj transakcję")

class CategoryForm(FlaskForm):
    name = StringField("Nazwa kategorii", validators=[DataRequired()])
    submit = SubmitField("Dodaj kategorię")

