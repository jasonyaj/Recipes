from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask_app.models import users_model
from flask import flash
from pprint import pprint

class Recipe:
    def __init__(self, data):
        self.id = data['id']
        self.users_id = data['users_id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.cooked_date = data['cooked_date']
        self.under_thirty = data['under_thirty']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user = None
    
    # add a new recipe to the recipes table
    @classmethod
    def create_one(cls,data):
        query = """
            INSERT INTO recipes (users_id, name, description, instructions, cooked_date, under_thirty)
            VALUES (%(users_id)s, %(name)s, %(description)s, %(instructions)s, %(cooked_date)s, %(under_thirty)s);
        """
        result = connectToMySQL( DATABASE ).query_db( query, data )
        return result

    # grab info of one recipe with created by user from recipes table
    @classmethod
    def get_one_with_user(cls,data):
        query = """
            SELECT *
            FROM recipes r JOIN users u
            ON u.id = r.users_id
            WHERE r.id = %(recipe_id)s;
        """
        result = connectToMySQL( DATABASE ).query_db( query, data )
        row = result[0]
        current_recipe = cls(row)
        current_user = {
            "id" : row['u.id'],
            "first_name" : row['first_name'],
            "last_name" : row['last_name'],
            "email" : row['email'],
            "password" : row['password'],
            "created_at" : row['u.created_at'],
            "updated_at" : row['u.updated_at']
        }
        current_recipe.user = users_model.User( current_user )
        return current_recipe

    # retrieve one recipe by id from recipes table
    @classmethod
    def get_one(cls,data):
        query = """
            SELECT *
            FROM recipes
            WHERE id = %(recipe_id)s;
        """
        result = connectToMySQL( DATABASE ).query_db( query, data )
        current_recipe = cls(result[0])
        return current_recipe

    # update one recipe
    @classmethod
    def update_one( cls, data ):
        query  = """
            UPDATE recipes
            SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, cooked_date = %(cooked_date)s, under_thirty = %(under_thirty)s
            WHERE id = %(recipe_id)s;
        """

        result = connectToMySQL( DATABASE ).query_db( query, data )
        return result

    # delete one recipe by id from recipes table
    @classmethod
    def delete_one(cls,data):
        query = """
            DELETE FROM recipes
            WHERE id = %(recipe_id)s;
        """
        result = connectToMySQL( DATABASE ).query_db( query, data )
        return result

    # grab all recipes with the created by user
    @classmethod
    def get_all_recipes_with_users(cls):
        query = """
            SELECT *
            FROM recipes r JOIN users u
            ON u.id = r.users_id
        """
        result = connectToMySQL( DATABASE ).query_db( query )
        list_of_recipes = []
        
        for row in result:
            current_recipe =cls(row) # cls is instances and row is a dictionary to populate the attributes
            user = {
                'id': row['u.id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'password': row['password'],
                'created_at': row['u.created_at'],
                'updated_at': row['u.updated_at']
            }
            current_user= users_model.User(user) # creates object of the user
            current_recipe.user = current_user # insert object-user into Recipe
            list_of_recipes.append(current_recipe) # appends new object into the list_of_recipes
        return list_of_recipes

    # method to validate adding and editing recipe from by setting parameters
    @staticmethod
    def validate_recipe(new_recipe):
        is_valid = True

        if len(new_recipe['name']) < 3:
            flash("Please provide a recipe name. At least 3 characters.", 'error_name')
            is_valid = False
        if len(new_recipe['description']) < 3:
            flash("Please provide a recipe description. At least 3 characters.", 'error_description')
            is_valid = False
        if len(new_recipe['instructions']) < 3:
            flash("Please provide cooking instructions. At least 3 characters.", 'error_instructions')
            is_valid = False
        if len(new_recipe['cooked_date']) < 3:
            flash("Date is required.", 'error_cooked_date')
            is_valid = False
        if "under_thirty" not in new_recipe:
            flash("Does your recipe take less then 30 minutes?", 'error_under_thirty')
            is_valid = False
        
        return is_valid