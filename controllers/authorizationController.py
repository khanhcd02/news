from flask import Blueprint, request,render_template,session,redirect
from models.authorization import Authorization
from models.dbconnect import DatabaseConnection
authorization_blueprint = Blueprint('users', __name__)
db_connection = DatabaseConnection()

@authorization_blueprint.route('/admin/authorization/create', methods=['GET','POST'])
def create_authorization():
    if 'user_id' not in session:
        return redirect('/login')
    elif 'access_rights' in session:
        access_rights = session.get('access_rights')
        if access_rights[0]['ManageAuthorization'] == 0:
            return redirect("/")
        else:
            author = Authorization(db_connection)
            if request.method == 'POST':            
                author.user_id = request.form['user_id']
                if 'news' in request.form:
                    author.manage_news = 1
                else:
                    author.manage_news = 0

                if 'users' in request.form:
                    author.manage_users = 1
                else:
                    author.manage_users = 0

                if 'bookmarks' in request.form:
                    author.manage_bookmarks = 1
                else:
                    author.manage_bookmarks = 0

                if 'categories' in request.form:
                    author.manage_categories = 1
                else:
                    author.manage_categories = 0

                if 'comments' in request.form:
                    author.manage_comments = 1
                else:
                    author.manage_comments = 0

                if 'authorization' in request.form:
                    author.manage_authorization = 1
                else:
                    author.manage_authorization = 0

                author.add_authorization()
                return redirect('/admin/authorization')
            users = author.list_user_need_permission()
            return render_template('admin/authorization/authorizationCreate.html', users = users, access = access_rights[0])
    return redirect("/")

@authorization_blueprint.route('/admin', methods=['GET'])
def admin():
    if 'user_id' not in session:
        return redirect('/login')
    elif 'access_rights' in session:
        access_rights = session.get('access_rights')
        if access_rights[0]['ManageAuthorization'] + access_rights[0]['ManageNews'] + access_rights[0]['ManageUsers'] + access_rights[0]['ManageBookmarks'] + access_rights[0]['ManageCategories'] + access_rights[0]['ManageComments'] == 0:
            return redirect("/")
        else:
            return render_template('admin/adminHome.html', access=access_rights[0])
    return redirect("/")
        
@authorization_blueprint.route('/admin/authorization', methods=['GET'])
def admin_authorization():
    if 'user_id' not in session:
        return redirect('/login')
    elif 'access_rights' in session: 
        access_rights = session.get('access_rights')        
        if access_rights[0]['ManageAuthorization'] == 0:
            return redirect("/")
        else:
            author = Authorization(db_connection)
            data = author.get_all_authorizations()
            return render_template('admin/authorization/authorizationList.html', data=data, access = access_rights[0])
    return redirect("/")

@authorization_blueprint.route('/admin/authorization/<int:id>', methods=['GET','POST'])
def update_authorization(id):
    if 'user_id' not in session:
        return redirect('/login')
    elif 'access_rights' in session: 
        access_rights = session.get('access_rights')
        if access_rights[0]['ManageAuthorization'] == 0:
            return redirect("/")
        else:
            author_update = Authorization(db_connection)
            author_update.user_id = id
            if request.method == 'POST':
                if 'news' in request.form:
                    author_update.manage_news = 1
                else:
                    author_update.manage_news = 0

                if 'users' in request.form:
                    author_update.manage_users = 1
                else:
                    author_update.manage_users = 0

                if 'bookmarks' in request.form:
                    author_update.manage_bookmarks = 1
                else:
                    author_update.manage_bookmarks = 0

                if 'categories' in request.form:
                    author_update.manage_categories = 1
                else:
                    author_update.manage_categories = 0

                if 'comments' in request.form:
                    author_update.manage_comments = 1
                else:
                    author_update.manage_comments = 0

                if 'authorization' in request.form:
                    author_update.manage_authorization = 1
                else:
                    author_update.manage_authorization = 0

                author_update.update_authorization()
                return redirect('/admin/authorization')
            item = author_update.check_access(id)
            return render_template('admin/authorization/authorizationUpdate.html', item=item[0], access = access_rights[0])
    return redirect("/")    