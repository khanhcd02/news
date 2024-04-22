from flask import Blueprint, request,render_template
from models.news import News
from models.categories import Category
from models.users import User
from models.dbconnect import DatabaseConnection

search_blueprint = Blueprint('search', __name__)
db_connection = DatabaseConnection()

news = News(db_connection)
categories = Category(db_connection)
user = User(db_connection)

@search_blueprint.route('/search', methods=['POST'])
def search_news():
    keyword = request.form['keyword']
    hot_news = news.get_hot_news()
    all_categories = categories.get_all_categories()
    results = news.get_news_by_keyword(keyword)
    author = user.get_author_by_keyword(keyword)
    return render_template('search.html', categories=all_categories, data = hot_news, results = results,author = author, keyword = keyword)
