from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired

class TransactionForm(FlaskForm):
    amount = FloatField("Kwota", validators=[DataRequired()])
    description = StringField("Opis")
    is_income = BooleanField("Dochód?")
    category = SelectField("Kategoria", coerce=int)
    submit = SubmitField("Dodaj transakcję")

