from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE, EMAIL_REGEX, app
from flask import flash
from flask_bcrypt import Bcrypt
from pprint import pprint
from flask_app.models import users_model, recipes_model

bcrypt = Bcrypt(app)

class User:

    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.list_of_recipes = [] # cant get appended to

    # add one user into the database
    @classmethod
    def create_one(cls, data):
        query = """
            INSERT INTO users( first_name, last_name, email, password ) 
            VALUES ( %(first_name)s, %(last_name)s, %(email)s, %(password)s );
        """
        result = connectToMySQL(DATABASE).query_db(query, data)
        return result

    # retrieve one user by email, used for login validation
    @classmethod
    def get_one_by_email(cls, data):
        query = """
            SELECT *
            FROM users
            WHERE email = %(email)s;
        """
        result = connectToMySQL(DATABASE).query_db(query, data)
        if len(result) == 0:
            flash("Email does not exist in our Database.", 'error_login_email')
            return None
        else:
            current_user = cls(result[0])
            return current_user

    # checks entered email against database in case of duplication, used for registration
    @classmethod
    def check_email(cls, data):
        query = """
            SELECT email
            FROM users
            WHERE email = %(email)s;
        """
        result = connectToMySQL(DATABASE).query_db(query, data)
        if len(result) == 0:
            return True
        else:
            flash("Email already in use. Please provide a different email.", 'error_register_email')
            return False

    # set requirements to be checked when user registers
    @staticmethod
    def validate_user(new_user):
        is_valid = True

        if len(new_user['first_name']) < 3:
            flash("You must provide your first name. At least 3 letters.",
                "error_first_name")
            is_valid = False
        if len(new_user['last_name']) < 3:
            flash("You must provide your last name. At least 3 letters.",
                "error_last_name")
            is_valid = False
        if len(new_user['password']) <= 8:
            flash("Your password must have at least have 8 characters.",
                "error_password")
            is_valid = False
        if new_user['password'] != new_user['confirm_password']:
            flash("Your passwords did not match.", "error_confirm_password")
            is_valid = False
        if not EMAIL_REGEX.match(new_user['email']):
            flash("Please provide a valid email address.", "error_email")
            is_valid = False

        return is_valid

    # encrypts the passed in string, used for password
    @staticmethod
    def encrypt_string(text):
        encrypted_string = bcrypt.generate_password_hash(text)
        return encrypted_string

    # checks to see if entered password matches database password
    @staticmethod
    def validate_password(plain_password, hashed_password):
        if not bcrypt.check_password_hash(hashed_password, plain_password):
            flash("Wrong password", 'error_login_password')
            return False
        else:
            return True
