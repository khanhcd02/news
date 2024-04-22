from flask import Blueprint, request,render_template,session,g,url_for,redirect,flash
from models.users import User
from models.dbconnect import DatabaseConnection
from models.authorization import Authorization
from werkzeug.utils import secure_filename
import os
users_blueprint = Blueprint('users', __name__)
db_connection = DatabaseConnection()
user = User(db_connection)
authorization = Authorization(db_connection)
@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        userlogin = User(db_connection)
        userlogin.username = request.form['username']
        userlogin.password = request.form['password']
        result = userlogin.login()
        if result:
            if result[0]['Status']!=0:
                session.clear()
                flash('Đăng nhập thành công', 'success')
                session['user_id'] = result[0]['Id']
                session['Name'] = result[0]['Name']
                if authorization.check_access(result[0]['Id']):
                    session['access_rights'] = authorization.check_access(result[0]['Id'])
                return redirect("/")
            else:
                return render_template('login.html', ban="Tài khoản này đã bị khoá!")
        else:
            return render_template('login.html', ban="Tên đăng nhập hoặc mật khẩu không đúng!")
    session.clear()
    return render_template('login.html')

@users_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        userRegister = User(db_connection)
        userRegister.name = request.form['name']
        userRegister.image = request.form['image']
        userRegister.username = request.form['username']
        userRegister.password = request.form['password']
        userRegister.email = request.form['email']
        userRegister.birth_day = request.form['birthday']
        userRegister.phone_number = request.form['phonenumber']
        userRegister.address = request.form['address']
        userRegister.status = request.form['status']
        result = userRegister.check_username()
        if result:
            return render_template('register.html',ban="Tài khoản đã tồn tại!")
        else:
            userRegister.register()
            # create_authorization(insert_id[0]['Id'])
            return redirect("/login")
    return render_template('register.html')
    
@users_blueprint.route('/admin/users', methods=['GET'])
def list_user():
    if 'user_id' not in session:
        return redirect('/login')
    elif 'access_rights' in session:
        access_rights = session.get('access_rights')
        if access_rights[0]['ManageUsers'] == 0:
            return redirect("/")
        else:
            list_users = user.get_all_users()
            return render_template("admin/users/usersList.html", data = list_users, access=access_rights[0])
    return redirect("/")

@users_blueprint.route('/admin/users/<int:id>', methods=['GET', 'POST'])
def detail_user(id):
    if 'user_id' not in session:
        return redirect('/login')
    elif 'access_rights' in session:
        access_rights = session.get('access_rights')
        if access_rights[0]['ManageUsers'] == 0:
            return redirect("/")
        else:
            if request.method == 'POST':
                img = request.files['img']
                if img:
                    filename = secure_filename(img.filename)
                    img.save(os.path.join(g.app.root_path, 'static', 'img', 'users', filename))
                    img_path = url_for('static', filename='img/users/' + filename)
                else:
                    img_path = request.form['image_url']
                    if img_path == '':
                        img_path = request.form['image']
                update_user = User(db_connection)
                update_user.id = id
                update_user.name = request.form['name']
                update_user.image = img_path
                update_user.birth_day = request.form['birthday']
                update_user.email = request.form['email']
                update_user.phone_number = request.form['phone']
                update_user.password = request.form['password']
                update_user.address = request.form['address']
                update_user.status = request.form['status']
                update_user.update_user()
                return redirect('/admin/users')
            user_update = user.get_user_by_id(id)
            return render_template("admin/users/updateUser.html", user = user_update[0], access=access_rights[0])
    return redirect("/")