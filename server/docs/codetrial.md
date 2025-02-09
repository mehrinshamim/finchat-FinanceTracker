@app.route('/add-expense', methods=['GET', 'POST'])
@login_required
def add_expense():
    form = ExpenseForm()
    if form.validate_on_submit():
        category = Category(name=form.category.data, user_id=current_user.id)
        db.session.add(category)
        db.session.commit()  # Commit the category to the database
        expense = Transaction(
            user_id=current_user.id,
            transaction_type='expense',
            amount=form.amount.data,
            category_id=category.id,  # Now category.id is not None
            description=form.description.data
        )
        db.session.add(expense)
        db.session.commit()
        flash('Expense added successfully.')
        return redirect(url_for('index'))
    return render_template('add_expense.html', title='Add Expense', form=form)


@app.route('/add-income', methods=['GET', 'POST'])
@login_required
def add_income():
    form = IncomeForm()
    if form.validate_on_submit():
        category = Category(name=form.category.data, user_id=current_user.id)
        db.session.add(category)
        db.session.commit()  # Commit the category to the database
        income = Transaction(
            user_id=current_user.id,
            transaction_type='income',
            amount=form.amount.data,
            category_id=category.id,  # Now category.id is not None
            description=form.description.data
        )
        db.session.add(income)
        db.session.commit()
        flash('Income added successfully.')
        return redirect(url_for('index'))
    return render_template('add_income.html', title='Add Income', form=form)