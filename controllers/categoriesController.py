from flask import render_template, request, redirect,session,Blueprint
from models.categories import Category
from models.dbconnect import DatabaseConnection
categories_blueprint = Blueprint('categories', __name__)
db_connection = DatabaseConnection()
categories = Category(db_connection)

@categories_blueprint.route('/admin/categories', methods=['GET'])
def display_categories():
    if 'user_id' not in session:
        return redirect('/login')
    elif 'access_rights' in session:
        access_rights = session.get('access_rights')
        if access_rights[0]['ManageCategories'] == 0:
            return redirect("/")
        else:
            categories_list = categories.get_all_categories()
            return render_template('admin/categories/categoriesList.html', data=categories_list, access=access_rights[0])    
    return redirect("/")

@categories_blueprint.route('/admin/categories/create', methods=['GET','POST'])
def add_category():
    if 'user_id' not in session:
        return redirect('/login')
    elif 'access_rights' in session:
        access_rights = session.get('access_rights')
        if access_rights[0]['ManageCategories'] == 0:
            return redirect("/")
        else:
            if request.method == 'POST':
                categories.name = request.form['category_name']
                if request.form['parent_id'] == '':
                    categories.parent_id = None
                else: 
                    categories.parent_id = request.form['parent_id']
                categories.status = 1
                categories.add_category()
                return redirect("/admin/categories")
            categories_list = categories.get_all_categories()
            return render_template('admin/categories/addCategory.html', categories=categories_list,access=access_rights[0])
    return redirect("/")

@categories_blueprint.route('/admin/categories/<int:id>', methods=['GET','POST'])
def update_category(id):
    if 'user_id' not in session:
        return redirect('/login')
    elif 'access_rights' in session:
        access_rights = session.get('access_rights')
        if access_rights[0]['ManageCategories'] == 0:
            return redirect("/")
        else:
            if request.method == 'POST':
                categories.id = id
                categories.name = request.form['category_name']
                if request.form['parent_id'] == '':
                    categories.parent_id = None
                else: 
                    categories.parent_id = request.form['parent_id']
                categories.status = request.form['status']
                categories.update_category()
                return redirect("/admin/categories")
            category = categories.get_category_by_id(id)
            categories_list = categories.get_all_categories()
            return render_template('admin/categories/updateCategory.html',categories=categories_list, category=category[0],access=access_rights[0])
    return redirect("/")
