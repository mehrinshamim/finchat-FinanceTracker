from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime , timezone, date
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
#from sqlalchemy import Enum
from app import db
from app import login

#class TransactionType(Enum):
#   income = 'income'
#   expense = 'expense'
#   loan = 'loan'

class User(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    timestamp: so.Mapped[datetime] = so.mapped_column(
        index=True, default=lambda: datetime.now(timezone.utc))

    categories: so.WriteOnlyMapped['Category'] = so.relationship(back_populates='creator')
    transactions: so.WriteOnlyMapped['Transaction'] = so.relationship(back_populates='creator')
    budgets: so.WriteOnlyMapped['Budget'] = so.relationship(back_populates='creator')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    
    def __repr__(self):
        return '<User {}>'.format(self.username)


@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))


class Category(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column( sa.String(50), index=True, unique=False)
    user_id: so.Mapped[int] = so.mapped_column( sa.ForeignKey(User.id), index=True)
    transaction_type: so.Mapped[str] = so.mapped_column(
        sa.String(50),
        index=True,
        unique=False,
        server_default='select'  # set default value to 'income'
    )
    deleted: so.Mapped[bool] = so.mapped_column(default=False,unique=False)  # Add a deleted column


    
    creator: so.Mapped[User] = so.relationship(back_populates='categories')
    transactions: so.WriteOnlyMapped['Transaction'] = so.relationship(back_populates='section')
    budgets: so.WriteOnlyMapped['Budget'] = so.relationship(back_populates='section')

    def __repr__(self):
        return '<Category {}>'.format(self.name)
    
class Transaction(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    amount: so.Mapped[float] = so.mapped_column(sa.Float(30),index=True)
    transaction_type: so.Mapped[str] = so.mapped_column(sa.String(50),index=True, unique=False) #should be income/expense/reimbursement
    description: so.Mapped[str] = so.mapped_column(sa.String(200),unique=False, nullable=False)  #how to add nullable=?
    category_id: so.Mapped[int] = so.mapped_column( sa.ForeignKey(Category.id),index=True)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)
    date : so.Mapped[datetime.date] = so.mapped_column( sa.Date, index=True, default= date.today)    #blackbox helped
    loan_type: so.Mapped[str] = so.mapped_column(sa.String(30), index=True, unique=False, nullable=True) #should be lent/received
    #related_transaction_id: 

    creator: so.Mapped[User] = so.relationship(back_populates='transactions')
    section: so.Mapped[Category] = so.relationship(back_populates='transactions')
    #transactions:
    #should i make a relnship for related_transaction_id???

    def __repr__(self):
        return '<Transaction amount {} for {}>'.format(self.amount, self.description)
## is it ok/will it work if i put Table?Modelname instead of self?

class Budget(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    amount: so.Mapped[float] = so.mapped_column(sa.Float(100),index=True)
    category_id: so.Mapped[int] = so.mapped_column( sa.ForeignKey(Category.id),index=True)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)
    start_date: so.Mapped[date] = so.mapped_column(sa.Date, nullable=False)
    end_date: so.Mapped[date] = so.mapped_column( sa.Date , nullable=False )

    creator: so.Mapped[User] = so.relationship(back_populates='budgets')
    section: so.Mapped[Category] = so.relationship(back_populates='budgets')

    def __repr__(self):
        return '<Budget amount {} from {} to {}>'.format(self.amount,self.start_date,self.end_date)


