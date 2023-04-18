from flask import session, render_template, request, redirect
from flask_app import app
from flask_app.models.users_model import User
from flask_app.models import recipes_model
from pprint import pprint

# homepage including registration form and login
@app.route('/')
def display_login_registration():
    return render_template('index.html')

# page used to collect, validate, and transfer new user info
@app.route('/process', methods=['POST'])
def register_user():
    new_user = {
        **request.form
    }
    data = {
        'email' : request.form['email']
    }
    if User.check_email(data) == False:
        return redirect( "/" )
    if User.validate_user( new_user ) == False:
        return redirect( "/" )
    else:
        new_user['password'] = User.encrypt_string(new_user['password'])
        user_id = User.create_one( new_user )
        session['user_id'] = user_id
        session['full_name'] = new_user['first_name'] + " " + new_user['last_name']
        return redirect( "/user" )

# user logged in and displays all recipes
@app.route('/user')
def user():
    if "user_id" not in session:
        return render_template('no_session.html')
    list_of_recipes = recipes_model.Recipe.get_all_recipes_with_users()
    return render_template('user.html', list_of_recipes=list_of_recipes)

# page to reset session, used for logging out
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

# page to check for login credentials
@app.route('/login', methods=['POST'])
def login():
    data = {
        'email' : request.form['email']
    }
    current_user = User.get_one_by_email(data)
    if current_user == None:
        return redirect('/')
    else:
        if User.validate_password(request.form['password'], current_user.password) == False:
            return redirect('/')
        else:
            session['user_id'] = current_user.id
            session['full_name'] = current_user.first_name + " " + current_user.last_name
            return redirect('/user')