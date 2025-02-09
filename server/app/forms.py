from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, IntegerField, PasswordField, BooleanField, SubmitField, DecimalField, TextAreaField, SelectField, HiddenField, FloatField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, NumberRange
import sqlalchemy as sa
from app import db
from app.models import User, Category

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')]
    )
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = db.session.scalar(sa.select(User).where(
            User.username == username.data
        ))
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = db.session.scalar(sa.select(User).where(
            User.email == email.data
        ))
        if user is not None:
            raise ValidationError('Please use a different email address.')

class ExpenseForm(FlaskForm):
    category = SelectField('Category', validators=[DataRequired()], coerce=int)
    description = TextAreaField('Description', validators=[DataRequired()])
    amount = DecimalField('Amount', validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField('Add Expense')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.category.choices = [(c.id, c.name) for c in db.session.scalars(sa.select(Category).where(Category.user_id == current_user.id, Category.transaction_type == 'expense', Category.deleted == False))]
class IncomeForm(FlaskForm):
    category = SelectField('Category', validators=[DataRequired()], coerce=int)
    description = TextAreaField('Description', validators=[DataRequired()])
    amount = DecimalField('Amount', validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField('Add Income')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.category.choices = [(c.id, c.name) for c in db.session.scalars(sa.select(Category).where(Category.user_id == current_user.id, Category.transaction_type == 'income', Category.deleted == False))]

#CATEGORY
class CategoryForm(FlaskForm):
    name = StringField('Category Name', validators=[DataRequired()])
    submit = SubmitField('Add Category')

class RenameCategoryForm(FlaskForm):
    category_id = IntegerField('Category ID', validators=[DataRequired()])
    new_name = StringField('New Category Name', validators=[DataRequired()])
    submit = SubmitField('Rename Category')

class DeleteCategoryForm(FlaskForm):
    category_id = IntegerField('Category ID', validators=[DataRequired()])
    submit = SubmitField('Delete Category')

class LentMoneyForm(FlaskForm):
    description = TextAreaField('Description', validators=[DataRequired()])
    amount = DecimalField('Amount', validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField('Add Expense')

#check semantics here
class UpdateTransactionForm(FlaskForm):
    transaction_id = HiddenField('Transaction ID')
    amount = FloatField('Amount', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Update')

class DeleteTransactionForm(FlaskForm):
    transaction_id = HiddenField('Transaction ID')
    submit = SubmitField('Delete')

class UpdatePasswordForm(FlaskForm):
    current_password = PasswordField('Enter Current Password', validators=[DataRequired()])
    new_password = PasswordField('Enter New Password', validators=[DataRequired()])
    confirm_new_password = PasswordField('Confirm New Password', validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Update Password')