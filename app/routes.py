from flask import render_template, flash, redirect, url_for, request
from urllib.parse import urlsplit
from app import app
from app.forms import LoginForm, RegistrationForm, ExpenseForm, IncomeForm, CategoryForm, RenameCategoryForm, DeleteCategoryForm, LentMoneyForm, UpdateTransactionForm, DeleteTransactionForm, UpdatePasswordForm

from flask_login import current_user, login_user, logout_user, login_required
import sqlalchemy as sa
from app import db
from app.models import User, Transaction, Category

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
    user = db.session.scalar(sa.select(User).where(User.username == username))
    if user is None:
        flash('User not found.')
        return redirect(url_for('index'))
    return render_template('user.html', user=user)

@app.route('/update-user-info', methods=['GET', 'POST'])
@login_required
def update_user_info():
    # Implement the logic to update user information
    pass


'''
-also include update password
- delete user data (also delete all transaction history [popup])
'''

@app.route('/update-password', methods=['GET', 'POST'])
@login_required
def update_password():
    form = UpdatePasswordForm()
    if form.validate_on_submit():
        if current_user.check_password(form.current_password.data):
            current_user.set_password(form.new_password.data)
            db.session.commit()
            flash('Password updated successfully.')
            return redirect(url_for('index'))
        else:
            flash('Invalid current password.')
    return render_template('update_password.html', title='Update Password', form=form)


@app.route('/delete-user', methods=['POST'])
@login_required
def delete_user():
    # Implement the logic to delete the user and associated data
    pass


# MONEY
@app.route('/add-expense', methods=['GET', 'POST'])
@login_required
def add_expense():
    form = ExpenseForm()
    if form.validate_on_submit():
        # Check if category exists, if not create a new one
        category = Category.query.filter_by(name=form.category.data, user_id=current_user.id, deleted=False).first()
        if not category:
            category = Category(name=form.category.data, user_id=current_user.id)
            db.session.add(category)
            db.session.commit()
        
        # Add expense with the category's id
        transaction = Transaction(amount=form.amount.data, transaction_type='expense', description=form.description.data, category_id=category.id, user_id=current_user.id, loan_type='None')
        db.session.add(transaction)
        db.session.commit()
        flash('Expense added successfully.')
        return redirect(url_for('view_expenses'))
    return render_template('add_expense.html', title='Add Expense', form=form, Category=Category)


@app.route('/add-income', methods=['GET', 'POST'])
@login_required
def add_income():
    form = IncomeForm()
    if form.validate_on_submit():
        # Check if category exists, if not create a new one
        category = Category.query.filter_by(name=form.category.data, user_id=current_user.id, deleted=False).first()
        if not category:
            category = Category(name=form.category.data, user_id=current_user.id)
            db.session.add(category)
            db.session.commit()
        
        # Add income with the category's id
        transaction = Transaction(amount=form.amount.data, transaction_type='income', description=form.description.data, category_id=category.id, user_id=current_user.id, loan_type='None')
        db.session.add(transaction)
        db.session.commit()
        flash('Income added successfully.')
        return redirect(url_for('view_incomes'))
    return render_template('add_income.html', title='Add Income', form=form, Category=Category)

##########      LOAN

@app.route('/add-lent-money', methods=['GET', 'POST'])
@login_required
def add_lent_money():
    form = LentMoneyForm()  
    if form.validate_on_submit():
        category = Category.query.filter_by(name='Loan', user_id=current_user.id).first()
        if category:
            if category.deleted:
                category.deleted = False
                db.session.commit()
        else:
            category = Category(name='Loan', user_id=current_user.id, transaction_type='loan')
            db.session.add(category)
            db.session.commit()

        transaction = Transaction(amount=form.amount.data, transaction_type='loan', description=form.description.data, category_id=category.id, user_id=current_user.id, loan_type='lent')
        db.session.add(transaction)
        db.session.commit()
        flash('Lent money added successfully.')
        return redirect(url_for('view_lent_money'))
    return render_template('add_lent_money.html', title='Add Lent Money', form=form)


@app.route('/view-lent-money')
@login_required
def view_lent_money():
    lent_transactions = db.session.scalars(sa.select(Transaction).where(Transaction.user_id == current_user.id, Transaction.loan_type == 'lent'))
    return render_template('view_lent_money.html', lent_transactions=lent_transactions)

@app.route('/reimburse/<int:transaction_id>', methods=['POST'])
@login_required
def reimburse(transaction_id):
    transaction = db.session.scalar(sa.select(Transaction).where(Transaction.id == transaction_id, Transaction.user_id == current_user.id))
    if transaction and transaction.loan_type == 'lent':
        transaction.loan_type = 'reimbursed'
        db.session.commit()
        flash('Loan marked as reimbursed.')
    else:
        flash('Transaction not found or not a lent transaction.')
    return redirect(url_for('view_lent_money'))
############################
'''
@app.route('/view-transactions')
@login_required
def view_transactions():
    transactions = db.session.scalars(sa.select(Transaction).where(Transaction.user_id == current_user.id))
    return render_template('view_transactions.html', transactions=transactions)
'''
@app.route('/view-transactions', methods=['GET', 'POST'])
@login_required
def view_transactions():
    update_form = UpdateTransactionForm()
    delete_form = DeleteTransactionForm()
    transactions = db.session.scalars(sa.select(Transaction).where(Transaction.user_id == current_user.id))
    
    if update_form.validate_on_submit():
        transaction = Transaction.query.filter_by(id=update_form.transaction_id.data, user_id=current_user.id).first()
        if transaction:
            transaction.amount = update_form.amount.data
            transaction.description = update_form.description.data
            db.session.commit()
            flash('Transaction updated successfully.')
            return redirect(url_for('view_transactions'))
        else:
            flash('Transaction not found.')
    
    if delete_form.validate_on_submit():
        transaction = Transaction.query.filter_by(id=delete_form.transaction_id.data, user_id=current_user.id).first()
        if transaction:
            db.session.delete(transaction)
            db.session.commit()
            flash('Transaction deleted successfully.')
            return redirect(url_for('view_transactions'))
        else:
            flash('Transaction not found.')
    
    return render_template('view_transactions.html', title='View Transactions', 
                           transactions=transactions, 
                           update_form=update_form, 
                           delete_form=delete_form)


@app.route('/view-expenses')
@login_required
def view_expenses():
    expenses = db.session.scalars(sa.select(Transaction).where(Transaction.user_id == current_user.id, Transaction.transaction_type == 'expense'))
    return render_template('view_expenses.html', expenses=expenses)

@app.route('/view-incomes')
@login_required
def view_incomes():
    incomes = db.session.scalars(sa.select(Transaction).where(Transaction.user_id == current_user.id, Transaction.transaction_type == 'income'))
    return render_template('view_incomes.html', incomes=incomes)

   #optional fns
@app.route('/update-entry', methods=['GET', 'POST'])
@login_required
def update_entry():
    # Implement the logic to update an entry
    pass

@app.route('/delete-entry', methods=['POST'])
@login_required
def delete_entry():
    # Implement the logic to delete an entry
    pass

## filter by transaction_type
## filter by category (mainly or only for expense)


# BUDGET
@app.route('/budget-report')
@login_required
def budget_report():
    # Implement the logic to generate budget reports
    pass

'''
- show weekly expense report
- monthly 
- yearly
'''

# CATEGORY
@app.route('/add-income-category', methods=['GET', 'POST'])
@login_required
def add_income_category():
    form = CategoryForm()
    if form.validate_on_submit():
        existing_category = Category.query.filter_by(name=form.name.data, user_id=current_user.id, transaction_type='income').first()
        if existing_category:
            if existing_category.deleted:
                existing_category.deleted = False
                db.session.commit()
                flash('Income category restored successfully.')
                return redirect(url_for('view_categories'))
            else:
                flash('Income category already exists.')
                return redirect(url_for('view_categories'))
        category = Category(name=form.name.data, user_id=current_user.id, transaction_type='income')
        db.session.add(category)
        db.session.commit()
        flash('Income category added successfully.')
        return redirect(url_for('view_categories'))
    return render_template('add_income_category.html', title='Add Income Category', form=form)

@app.route('/add-expense-category', methods=['GET', 'POST'])
@login_required
def add_expense_category():
    form = CategoryForm()
    if form.validate_on_submit():
        existing_category = Category.query.filter_by(name=form.name.data, user_id=current_user.id, transaction_type='expense').first()
        if existing_category:
            if existing_category.deleted:
                existing_category.deleted = False
                db.session.commit()
                flash('Expense category restored successfully.')
                return redirect(url_for('view_categories'))
            else:
                flash('Expense category already exists.')
                return redirect(url_for('view_categories'))
        category = Category(name=form.name.data, user_id=current_user.id, transaction_type='expense')
        db.session.add(category)
        db.session.commit()
        flash('Expense category added successfully.')
        return redirect(url_for('view_categories'))
    return render_template('add_expense_category.html', title='Add Expense Category', form=form)

@app.route('/view-categories', methods=['GET', 'POST'])
@login_required
def view_categories():
    add_category_form = CategoryForm()
    rename_category_form = RenameCategoryForm()
    delete_category_form = DeleteCategoryForm()
    categories = Category.query.filter_by(user_id=current_user.id, deleted=False).filter(Category.transaction_type != 'loan').all()
    if rename_category_form.validate_on_submit():
        category = Category.query.filter_by(id=rename_category_form.category_id.data, user_id=current_user.id).first()
        if category:
            category.name = rename_category_form.new_name.data
            db.session.commit()
            flash('Category renamed successfully.')
            return redirect(url_for('view_categories'))
        else:
            flash('Category not found.')

    if delete_category_form.validate_on_submit():
        category = Category.query.filter_by(id=delete_category_form.category_id.data, user_id=current_user.id).first()
        if category:
            db.session.delete(category)
            db.session.commit()
            flash('Category deleted successfully.')
            return redirect(url_for('view_categories'))
        else:
            flash('Category not found.')

    return render_template('view_categories.html', title='View Categories', 
                           categories=categories, 
                           rename_category_form=rename_category_form, 
                           delete_category_form=delete_category_form)

# Rename Category
@app.route('/rename-category', methods=['GET', 'POST'])
@login_required
def rename_category():
    form = RenameCategoryForm()
    if form.validate_on_submit():
        category = Category.query.filter_by(id=form.category_id.data, user_id=current_user.id).first()
        if category:
            category.name = form.new_name.data
            db.session.commit()
            flash('Category renamed successfully.')
            return redirect(url_for('view_categories'))
        else:
            flash('Category not found.')
    return render_template('rename_category.html', title='Rename Category', form=form)

# Delete Category
@app.route('/delete-category', methods=['POST'])
@login_required
def delete_category():
    form = DeleteCategoryForm()
    if form.validate_on_submit():
        category = Category.query.filter_by(id=form.category_id.data, user_id=current_user.id).first()
        if category:
            category.deleted = True
            db.session.commit()
            flash('Category deleted successfully.')
            return redirect(url_for('view_categories'))
        else:
            flash('Category not found.')
    return redirect(url_for('view_categories'))

'''
- list category
(- delete category
- rename category )
'''


#TESTING
@app.route('/testing')
@login_required
def testing():
    return render_template('testing.html', title='Testing Endpoints')