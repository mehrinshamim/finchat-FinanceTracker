# Finance Tracker Web Application

**FinChat** is a web-based personal finance tracker built using Flask & SQLite

https://finchat-financetracker.onrender.com

## Features:

- **User Authentication:** Secure login, registration, and user session management.
- **Expense Management:** Add, view, and categorize expenses.
- **Income Management:** Track various sources of income.
- **Lent Money Management:** Track money lent to others and manage repayments.
- **Category Management:** Create and manage financial categories.
- **Budget Reporting:** Generate weekly, monthly, and yearly expense reports.
- **Transaction Viewing:** Comprehensive view of all financial transactions.
- **User Management:** Update user information and change passwords.
- **Responsive Design:** Accessible on various devices with a modern and clean interface.

## Technology Stack:

- **Backend:** Flask, SQLAlchemy
- **Frontend:** HTML, CSS
- **Database:** SQLite 
- **Authentication:** Flask-Login
- **Forms:** Flask-WTF

## End Goal - FinChat
A personalized chatbot that helps you track your finances and gives you insights weekly or monthly on how much you've spent on each category of things at, you know, normal expenses.

## Current Status:
*I'm currently still working on this project (version 1.0 web version) to enhance its features and improve its usability. Stay tuned for updates!*

## Setup Instructions:
1. Clone the repository: `git clone https://github.com/mehrinshamim/finchat-FinanceTracker.git`
2. Create a virtual environment in the project directory: `python -m venv venv`
3. Activate the virtual environment: `venv/Scripts/activate`
4. Install the requirements: `pip install -r requirements.txt`
5. Initialize the migration repository: `flask db init` (only needed once)
6. Generate an initial migration: `flask db migrate -m "Initial migration."` (only needed once)
7. Apply the migration to the database: `flask db upgrade`
8. And finally, run the application: `flask run`
9. Access the application via the provided local server link.
