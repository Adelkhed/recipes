from flask_app.config.mysqlconnection import connectToMySQL, DB
from flask import flash

class Recipe:
    DB = "user_login_registration"

    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date_cooked = data['date_cooked']
        self.under_30_minutes = data['under_30_minutes']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user = None
    @classmethod
    def save(cls, data):
        query = """
        INSERT INTO recipes (name, description, instructions, date_cooked, under_30_minutes, user_id) 
        VALUES (%(name)s, %(description)s, %(instructions)s, %(date_cooked)s, %(under_30_minutes)s, %(user_id)s);
        """
        return connectToMySQL(DB).query_db(query, data)

    @classmethod
    def update(cls, data):
        query = """
        UPDATE recipes 
        SET name=%(name)s, description=%(description)s, instructions=%(instructions)s, date_cooked=%(date_cooked)s, under_30_minutes=%(under_30_minutes)s 
        WHERE id=%(id)s;
        """
        return connectToMySQL(DB).query_db(query, data)

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM recipes WHERE id = %(id)s;"
        return connectToMySQL(DB).query_db(query, data)

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM recipes WHERE id = %(id)s;"
        result = connectToMySQL(DB).query_db(query, data)
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recipes;"
        results = connectToMySQL(DB).query_db(query)
        recipes = []
        for row in results:
            recipes.append(cls(row))
        return recipes

    @staticmethod
    def validate_recipe(recipe):
        is_valid = True
        if len(recipe['name']) < 3:
            flash("Name must be at least 3 characters.", "recipe")
            is_valid = False
        if len(recipe['description']) < 3:
            flash("Description must be at least 3 characters.", "recipe")
            is_valid = False
        if len(recipe['instructions']) < 3:
            flash("Instructions must be at least 3 characters.", "recipe")
            is_valid = False
        if 'date_cooked' not in recipe or recipe['date_cooked'] == "":
            flash("Date cooked is required.", "recipe")
            is_valid = False
        if 'under_30_minutes' not in recipe:
            flash("Please select 'Yes' or 'No' for 'Under 30 Minutes?'", "recipe")
            is_valid = False
        elif recipe['under_30_minutes'] not in ['Yes', 'No']:
            flash("Invalid selection for 'Under 30 Minutes?'", "recipe")
            is_valid = False
        return is_valid
