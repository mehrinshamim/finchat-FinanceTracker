from datetime import datetime , timezone, date
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db


class User(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    timestamp: so.Mapped[datetime] = so.mapped_column(
        index=True, default=lambda: datetime.now(timezone.utc))

    categories: so.WriteOnlyMapped['Category'] = so.relationship(back_populates='creator')
    transactions: so.WriteOnlyMapped['Transaction'] = so.relationship(back_populates='creator')
    budgets: so.WriteOnlyMapped['Budget'] = so.relationship(back_populates='creator')


    
    def __repr__(self):
        return '<User {}>'.format(self.username)
    
class Category(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column( sa.String(50), index=True, unique=True)
    user_id: so.Mapped[int] = so.mapped_column( sa.ForeignKey(User.id), index=True)
    
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
    loan_type: so.Mapped[str] = so.mapped_column(sa.String(30), index=True, unique=False) #should be lent/received
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
