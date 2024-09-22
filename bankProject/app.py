import re
import random
from flask import Flask, redirect, request, jsonify, session, render_template, url_for

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Secret key for session management

users = {}
accounts = {}

class Account:
    def __init__(self, initial_balance=0):
        self.balance = initial_balance
        self.account_number = self.generate_account_number()

    @staticmethod
    def generate_account_number():
        """Generate a random 10-digit account number starting with '1'."""
        return '1' + ''.join(str(random.randint(0, 9)) for _ in range(9))

    def deposit(self, amount):
        if amount < 0:
            return "Invalid amount. Deposit cannot be negative."
        self.balance += amount
        return f"Deposit successful. New balance: ${self.balance:.2f}"

    def withdraw(self, amount):
        if amount > self.balance:
            return "Insufficient funds. Withdrawal denied."
        self.balance -= amount
        return f"Withdrawal successful. New balance: ${self.balance:.2f}"

    def transfer(self, recipient_account_number, amount):
        """Transfer an amount to another account using account number."""
        recipient = accounts.get(recipient_account_number)
        if recipient:
            if self.withdraw(amount) == f"Withdrawal successful. New balance: ${self.balance:.2f}":
                recipient.deposit(amount)
                return f"Transfer successful. ${amount:.2f} was transferred."
            else:
                return "Transfer failed. Unable to withdraw the full amount."
        else:
            return "Transfer failed. Recipient account not found."

    def display_balance(self):
        return f"Account Number: {self.account_number} - Current balance: ${self.balance:.2f}"

def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email)

@app.route('/')
def home():
    return render_template('login.html')

@app.route("/dashboard")
def dashboard():
    if 'username' not in session:
        return redirect(url_for('home'))
    return render_template('dashboard.html')

@app.route('/signup', methods=['POST'])
def sign_up():
    data = request.json
    email = data.get('email')
    username = data.get('username')
    password = data.get('password')

    if any(user['email'] == email for user in users.values()):
        return jsonify({"message": "Email already exists. Try a different email."}), 400

    if not is_valid_email(email):
        return jsonify({"message": "Invalid email format."}), 400

    if username in users:
        return jsonify({"message": "Username already exists. Try a different username."}), 400

    new_account = Account(100)  # Initial balance of $100
    users[username] = {'email': email, 'password': password, 'account_number': new_account.account_number}
    accounts[new_account.account_number] = new_account
    return jsonify({"message": "Sign up successful", "account_number": new_account.account_number}), 201

@app.route('/signin', methods=['POST'])
def sign_in():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if username not in users:
        return jsonify({"message": "Username does not exist."}), 400

    if users[username]['password'] == password:
        session['username'] = username
        return jsonify({"message": "Sign in successful."}), 200
    else:
        return jsonify({"message": "Incorrect password."}), 400

@app.route('/signout', methods=['POST'])
def sign_out():
    session.pop('username', None)
    return jsonify({"message": "Sign out successful."}), 200

@app.route('/deposit', methods=['POST'])
def deposit():
    if 'username' not in session:
        return jsonify({"message": "Please sign in first."}), 401

    data = request.json
    amount = float(data.get('amount'))
    account = accounts[users[session['username']]['account_number']]
    message = account.deposit(amount)
    return jsonify({"message": message}), 200

@app.route('/withdraw', methods=['POST'])
def withdraw():
    if 'username' not in session:
        return jsonify({"message": "Please sign in first."}), 401

    data = request.json
    amount = float(data.get('amount'))
    account = accounts[users[session['username']]['account_number']]
    message = account.withdraw(amount)
    return jsonify({"message": message}), 200

@app.route('/transfer', methods=['POST'])
def transfer():
    if 'username' not in session:
        return jsonify({"message": "Please sign in first."}), 401

    data = request.json
    recipient_account_number = data.get('recipient_account_number')
    amount = float(data.get('amount'))
    account = accounts[users[session['username']]['account_number']]
    message = account.transfer(recipient_account_number, amount)
    return jsonify({"message": message}), 200

if __name__ == '__main__':
    app.run(debug=True)
