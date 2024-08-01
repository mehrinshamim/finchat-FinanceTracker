from flask import render_template, flash, redirect, url_for, request
from urllib.parse import urlsplit
from app import app
from app.forms import LoginForm, RegistrationForm

from flask_login import current_user, login_user, logout_user, login_required
import sqlalchemy as sa
from app import db
from app.models import User

#WELCOME PAGE

@app.route('/')
@app.route('/index')
@login_required
def index():
    # ...
    return render_template("index.html", title='Home Page')


#USERS

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(sa.select(User).where(User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        
#        if not user.is_active:
#            flash('Your account is not active')
#            return redirect(url_for('login'))
        
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html',  title='Sign In', form=form)

#If the netloc is not empty, it means the next URL is an absolute URL (e.g., http://example.com/path) rather than a relative URL (e.g., /path).

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/<username>')
def user(username):
    # do something with the username
    pass

  #optional
def update_user_info():
    pass
'''
-also include update password
- delete user data (also delete all transaction history [popup])
'''


#MONEY
@app.route('/add-expense')
def add_expense():
    pass

@app.route('/add-income')
def add_income():
    pass

@app.route('/add-lent-money')
def add_lent_money():
    pass

@app.route('/get-back-money')
def get_back_money():
    pass


@app.route('/view-transactions')
def view_traansactions():
    pass
   
   #optional fns
def update_an_entry():
    pass

def delete_an_entry():
    pass

## filter by transaction_type
## filter by category (mainly or only for expense)


#BUDGET
@app.route('/budget-report')
def budget_report():
    pass

'''
- show weekly expense report
- monthly 
- yearly
'''

#CATEGORY
@app.route('/add-category')
def add_category():
    pass

'''
- list category
(- delete category
- rename category )
'''