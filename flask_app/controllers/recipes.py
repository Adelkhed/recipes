from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.recipe import Recipe

@app.route('/recipes')
def recipes_dashboard():
    if 'user_id' not in session:
        return redirect('/')
    recipes = Recipe.get_all()
    return render_template("dashboard.html", recipes=recipes)

@app.route('/recipes/new')
def new_recipe():
    if 'user_id' not in session:
        return redirect('/')
    return render_template("new_recipe.html")

@app.route('/recipes/create', methods=['POST'])
def create_recipe():
    if 'user_id' not in session:
        return redirect('/')
    if not Recipe.validate_recipe(request.form):
        return redirect('/recipes/new')
    data = {
        "name": request.form['name'],
        "description": request.form['description'],
        "instructions": request.form['instructions'],
        "date_cooked": request.form['date_cooked'],
        "under_30_minutes": request.form['under_30_minutes'],
        "user_id": session['user_id']
    }
    Recipe.save(data)
    return redirect('/recipes')

@app.route('/recipes/edit/<int:id>')
def edit_recipe(id):
    if 'user_id' not in session:
        return redirect('/')
    recipe = Recipe.get_by_id({"id": id})
    if recipe.user_id != session['user_id']:
        return redirect('/recipes')
    return render_template("edit_recipe.html", recipe=recipe)

@app.route('/recipes/update', methods=['POST'])
def update_recipe():
    if 'user_id' not in session:
        return redirect('/')
    if not Recipe.validate_recipe(request.form):
        return redirect(f'/recipes/edit/{request.form["id"]}')
    Recipe.update(request.form)
    return redirect('/recipes')

@app.route('/recipes/delete/<int:id>')
def delete_recipe(id):
    if 'user_id' not in session:
        return redirect('/')
    Recipe.delete({"id": id})
    return redirect('/recipes')

@app.route('/recipes/<int:id>')
def view_recipe(id):
    if 'user_id' not in session:
        return redirect('/')
    recipe = Recipe.get_by_id({"id": id})
    return render_template("view_recipe.html", recipe=recipe)
