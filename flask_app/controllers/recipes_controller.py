from flask import session, render_template, request, redirect
from flask_app import app
from flask_app.models.recipes_model import Recipe

# view a single recipe in detail
@app.route('/recipe/<int:id>')
def recipe(id):
    if "user_id" not in session:
        return render_template('no_session.html')
    data = {
        'recipe_id' : id
    }
    current_recipe = Recipe.get_one_with_user( data )
    return render_template('recipe.html', current_recipe = current_recipe)

# form to create a new recipe
@app.route('/recipe/new')
def create_recipe():
    if "user_id" not in session:
        return render_template('no_session.html')
    return render_template('new_recipe.html')

# page to validate, collect, and transfer NEW recipe data
@app.route('/recipe/process', methods=['POST'])
def process_recipe():
    if Recipe.validate_recipe (request.form) == False:
        return redirect('/recipe/new')
    
    new_recipe = {
        'users_id' : session['user_id'],
        'name' : request.form['name'],
        'description' : request.form['description'],
        'instructions' : request.form['instructions'],
        'cooked_date' : request.form['cooked_date'],
        'under_thirty' : request.form['under_thirty']
    }
    recipe_id = Recipe.create_one(new_recipe)
    return redirect('/user')

# edit current recipe form
@app.route('/recipe/<int:id>/edit')
def edit_recipe_form(id):
    if "user_id" not in session:
        return render_template('no_session.html')
    data = {
        'recipe_id' : id
    }
    current_recipe = Recipe.get_one(data)
    if current_recipe.users_id != session['user_id']: #checks recipe creater vs logged in user so they cant edit recipes not belonging to them
        return redirect('/user')
    return render_template('edit_recipe.html', current_recipe = current_recipe)

# page to validate, collect and transfer CURRENT recipe data
@app.route('/recipe/<int:id>/update', methods=["POST"])
def update_recipe(id):
    data = {
        'name': request.form['name'],
        'description': request.form['description'],
        'instructions': request.form['instructions'],
        'cooked_date': request.form['cooked_date'],
        'under_thirty': request.form['under_thirty'],
        'recipe_id' : id
    }
    current_recipe = Recipe.update_one(data)
    return redirect('/user')

# route used to delete one recipe
@app.route('/recipe/<int:id>/delete')
def delete_recipe(id):
    if "user_id" not in session:
        return render_template('no_session.html')
    data = {
        'recipe_id' : id
    }
    Recipe.delete_one(data)
    return redirect('/user')