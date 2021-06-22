from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
# from flask_bcrypt import Bcrypt
# from flask_app.models.ninja import ### other models ###


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Account:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @classmethod
    def get_all(cls):
        query = "SELECT * FROM accounts;"
        results = connectToMySQL('login_registration_schema').query_db(query)
        accounts = []
        for account in results:
            accounts.append(cls(account))
        print(accounts)
        return accounts

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM accounts WHERE email=%(email)s;"
        results = connectToMySQL('login_registration_schema').query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def delete(cls,data):
        query = "DELETE FROM accounts WHERE id=%(id)s"
        connectToMySQL('login_registration_schema').query_db(query,data)


    @classmethod
    def insert(cls, data):
        query = "INSERT INTO accounts (first_name,last_name,email,password,created_at, updated_at) VALUES( %(first_name)s,%(last_name)s,%(email)s,%(password)s,NOW(), NOW());"
        return connectToMySQL('login_registration_schema').query_db(query, data)


    @staticmethod  # make sure no duplicate email # has email structure
    def validate_user(data):
        is_valid = True # the keys must match the request.form keys or NAME in the HTML
        if len(data['first_name']) < 3:
            flash("Name must be at least 3 characters.",'name')
            is_valid = False
        if len(data['last_name']) < 3:
            flash("last must be at least 3 characters.","name")
            is_valid = False
        if not data['first_name'].isalpha():
            flash("May not contain non alphabetical characters","name")
        if not EMAIL_REGEX.match(data['email']): 
            flash("Invalid email address!",'emailError')
            is_valid = False
        elif Account.duplicates(data['email']):
            flash("Invalid email address!",'emailError')
            is_valid = False
        if len(data['password']) < 3:
            flash("password must be at least 3 characters.","password")
            is_valid = False
        if data['password'] != data['confirm']:
            flash("Passwords must Match","confirm")
        flash(f"You have successfully logged in with : {data['email']}","success")
        return is_valid

    @staticmethod
    def duplicates(data):
        query = "SELECT * FROM emails WHERE email=%(email)s;"
        result = connectToMySQL('login_registration_schema').query_db(query,data)
        duplicate = False
        if result:
            duplicate = True
        return duplicate
    # @staticmethod
    # def validate_email(email):
    #     is_valid = True
    #     # test whether a field matches the pattern
    #     if not EMAIL_REGEX.match(email['email']): 
    #         flash("Invalid email address!")
    #         is_valid = False
    #     return is_valid