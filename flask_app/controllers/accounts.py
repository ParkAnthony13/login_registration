import re
from flask_app import app
from flask import render_template, request, session, redirect, flash
from flask_app.models.account import Account
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
# from flask_app.models.ninja import Ninja


@app.route('/')
def home():
    return render_template('front_page.html')

@app.route('/process',methods=['POST'])
def new_account():
    if not Account.validate_user(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    data = {
        'first_name':request.form['first_name'],
        'last_name':request.form['last_name'],
        'email':request.form['email'],
        'password':pw_hash
    }
    user_id = Account.insert(data)
    session['user_id'] = user_id
    return redirect(f"/success/{user_id}")

@app.route('/login', methods=['POST'])
def login():
    data = {"email":request.form['login_email']}
    user_in_db = Account.get_by_email(data)
    print(user_in_db)
    if not user_in_db:
        flash("Invalid Email/Password","perror")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['login_password']):
        flash("Invalid Email/Password","perror")
    session['user_id'] = user_in_db.id
    return redirect(f"/success/{session['user_id']}")

@app.route('/success/<int:user_id>')
def successful(user_id):
    if 'user_id' not in session:
        return redirect('/')
    account = Account.get_all()
    return render_template('success.html',account_list=account,user_id=user_id)

@app.route('/delete/<int:id>')
def delete(id):
    Account.delete({'id':id})
    return redirect(f"/success/{session['user_id']}")

@app.route('/register', methods=['POST'])
def register():
    if not Account.validate_user(request.form):
        return redirect('/')
    return redirect(f"/success/{session['user_id']}")

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')