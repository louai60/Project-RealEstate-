from flask_app import app
from flask import abort, redirect, render_template, request, flash, session
from flask_app.models import user


@app.route("/home")
def home():

    return render_template("layout.html")

# @app.route("/recipes")
# def display_all_recipes():
#     #! Guard Route
#     if "user_id" not in session:
#         return redirect("/")
    
#     data = {"id": session["user_id"]}
#     current_user = user.User.get_by_id(data)
    
#     if current_user:
#         all_recipes_users = recipe.Recipe.get_all_with_users()
#         return render_template("recipes.html", username=current_user.first_name, all_recipes = all_recipes_users)
#     else:
#         flash("User not found", "user_error")
#         return redirect("/")
    
# # * View Route (Show the edit form)
# @app.route("/recipes/new")
# def display_create_recipe():
#     #! Guard Route
#     if "user_id" not in session:
#         return redirect("/")
#     return render_template("add_recipe.html")

# #! ACTION ROUTE (precess the updated recipe)
# @app.route('/recipes/process', methods=['POST'])
# def create():
#     #! Guard Route
#     if "user_id" not in session:
#         return redirect("/")
#     # Check if a recipe is valid
#     if not recipe.Recipe.validate_recipe(request.form):
#         return redirect('/recipes/new')
    
#     # Grab the user id from the session
#     data = {
#         **request.form,
#         "under": request.form.get("under") if request.form.get("under") == "yes" else "no",
#         "user_id": session["user_id"]
#     }

#     # Create the recipe to the database 
#     id = recipe.Recipe.create(data)
#     print("----------------",id)
#     return redirect(f'/recipes/{id}')



# @app.route('/recipes/<int:id>')
# def view_recipe(id):
#     #! Guard Route
#     if "user_id" not in session:
#         return redirect("/")
    
#     data = {
#         "id":id
#     }

#     one_recipe = recipe.Recipe.get_one_with_user(data)

#     # grab the user id from session and put it in dictionnary
#     user_id = {"id": session["user_id"]}
#     # grab the user by id from DB 
#     current_user = user.User.get_by_id(user_id)

#     return render_template('view_recipe.html', recipe=recipe.Recipe.get_by_id(data), username=current_user.first_name, creator = one_recipe)

# # * View Route (Show the edit form)
# @app.route('/recipes/edit/<int:id>')
# def display_edit_form(id):
#     #! Guard Route
#     if "user_id" not in session:
#         return redirect("/")
    
#     data = {"id": id}

#     recipe_data = recipe.Recipe.get_by_id(data)
#     date_inserted = recipe_data.date
#     under_value = recipe_data.under 
#     return render_template('edit_recipe.html', recipe = recipe.Recipe.get_by_id(data), date_inserted = date_inserted, under_value = under_value)

# #! ACTION ROUTE (precess the updated recipe)
# @app.route('/recipes/update/<int:id>', methods=['POST'])
# def process_updated_recipe(id):
#     #! Guard Route
#     if "user_id" not in session:
#         return redirect("/")
    
#     # Check if a recipe is valid
#     if not recipe.Recipe.validate_recipe(request.form):
#         return redirect(f'/recipes/edit/{id}')
    
#     # Grab the user id from the session
#     data = {
#         **request.form,
#         "under": request.form.get("under") if request.form.get("under") == "yes" else "no",  
#         "user_id": session["user_id"],
#         "id": id
#     }
#     # Update the recipe to the database 
#     recipe.Recipe.update(data)

#     return redirect('/recipes')

# #! ACTION ROUTE (Delete recipe)
# @app.route('/delete/<int:id>', methods=['POST'])
# def delete_recipe(id):
#     #! Guard Route
#     if "user_id" not in session:
#         return redirect("/")
#     recipe.Recipe.delete_recipe(id)
#     return redirect('/recipes')

