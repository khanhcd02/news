from flask import Blueprint, request, render_template,session,g,url_for,redirect
from models.news import News
from models.categories import Category
from models.users import User
from models.dbconnect import DatabaseConnection
from datetime import datetime
from werkzeug.utils import secure_filename
import os
news_blueprint = Blueprint('news', __name__)
db_connection = DatabaseConnection()

news = News(db_connection)
categories = Category(db_connection)
user = User(db_connection)
@news_blueprint.route('/', methods=['GET'])
def get_all_news():
    all_news = news.get_hot_news()
    all_categories = categories.get_all_categories()
    return render_template('index.html', data=all_news, categories=all_categories)

@news_blueprint.route('/admin/news', methods=['GET'])
def list_news():
    if 'user_id' not in session:
        return redirect('/login')
    elif 'access_rights' in session:
        access_rights = session.get('access_rights')
        if access_rights[0]['ManageNews'] == 0:
            return redirect("/")
        else:
            all_news = news.get_all_news()
            return render_template('/admin/news/newsList.html', data=all_news, access=access_rights[0])
    return redirect("/")

@news_blueprint.route('/admin/news/create', methods=['GET', 'POST'])
def create_news():
    if 'user_id' not in session:
        return redirect('/login')
    elif 'access_rights' in session:
        access_rights = session.get('access_rights')
        if access_rights[0]['ManageNews'] == 0:
            return redirect("/")
        else:
            if request.method == 'POST':
                img = request.files['img']
                if img:
                    filename = secure_filename(img.filename)
                    img.save(os.path.join(g.app.root_path, 'static', 'img', 'news', filename))
                    img_path = url_for('static', filename='img/news/' + filename)
                else:
                    img_path = request.form['image_url']
                create_news = News(db_connection)
                create_news.title = request.form['title']
                create_news.content = request.form['content']
                create_news.image = img_path
                create_news.author_id = session.get('user_id')
                create_news.published_at = datetime.now()
                create_news.category_id = request.form['category']
                create_news.status = 1
                create_news.add_news()
                return redirect('/admin/news')
            all_categories = categories.get_all_categories()
            return render_template('admin/news/createNews.html',categories=all_categories, access=access_rights[0])
    return redirect("/")

@news_blueprint.route('/<int:id>', methods=['GET'])
def read_news(id):
    hot_news = news.get_hot_news()
    news_detail = news.get_news_by_id(id)
    all_categories = categories.get_all_categories()
    return render_template('detail.html', data=hot_news, categories=all_categories, item = news_detail[0])

@news_blueprint.route('/category/<int:id>', methods=['GET'])
def news_by_category(id):
    hot_news = news.get_hot_news()
    result = news.get_news_by_category_id(id)
    all_categories = categories.get_all_categories()
    if result:
        note = "Các bài viết trong danh mục '"+result[0]['CategoryName']+"'"
    else:
        note = "Không tìm thấy bài viết nào"
    return render_template('category.html', categories=all_categories, data = hot_news, result = result,note=note)

@news_blueprint.route('/author/<int:id>', methods=['GET'])
def news_by_author(id):
    hot_news = news.get_hot_news()
    result = news.get_news_by_author_id(id)
    all_categories = categories.get_all_categories()
    if result:
        note = "Các bài viết của tác giả '"+result[0]['Author']+"'"
    else:
        note = "Không tìm thấy bài viết nào"
    return render_template('category.html', categories=all_categories, data = hot_news, result = result,note = note)

@news_blueprint.route('/admin/news/<int:id>', methods=['GET','POST'])
def update_news(id):
    if 'user_id' not in session:
        return redirect('/login')
    elif 'access_rights' in session:
        access_rights = session.get('access_rights')
        if access_rights[0]['ManageNews'] == 0:
            return redirect("/")
        else:
            if request.method == 'POST':
                img = request.files['img']
                if img:
                    filename = secure_filename(img.filename)
                    img.save(os.path.join(g.app.root_path, 'static', 'img', 'news', filename))
                    img_path = url_for('static', filename='img/news/' + filename)
                else:
                    img_path = request.form['image_url']
                    if img_path == '':
                        img_path = request.form['image']
                update_news = News(db_connection)
                update_news.id = id
                update_news.title = request.form['title']
                if request.form['content'] == '':
                    update_news.content = request.form['old_content']
                else:
                    update_news.content = request.form['content']
                update_news.image = img_path
                update_news.category_id = request.form['category']
                update_news.published_at = datetime.now()
                update_news.status = request.form['status']
                update_news.update_news()
                return redirect('/admin/news')
            news_update = news.get_news_by_id(id)
            all_categories = categories.get_all_categories()
            if news:
                return render_template('admin/news/updateNews.html', news=news_update[0], categories=all_categories, access=access_rights[0])
            else:
                return "Tin tức không tồn tại"
    return redirect("/")
        
