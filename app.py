from flask import Flask, render_template, send_from_directory, request, redirect, url_for, flash, session, g
from models.dbconnect import DatabaseConnection
from models.users import User
import bs4
import re
import requests
from datetime import datetime
from dateutil import parser
from controllers.searchController import search_blueprint
from controllers.newsController import news_blueprint
from controllers.usersController import users_blueprint
from controllers.authorizationController import authorization_blueprint
from controllers.categoriesController import categories_blueprint
app = Flask(__name__)
db_connection = DatabaseConnection()
app.secret_key = 'khanhcd02'
UPLOAD_FOLDER = '/static/img/news'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/<path:filename>')
def serve_img(filename):
    return send_from_directory('static/img', filename)

@app.route('/users/<path:filename>')
def user_img(filename):
    return send_from_directory('static/img/users', filename)

@app.route('/static/js/<path:filename>')
def serve_js(filename):
    return send_from_directory('static/js', filename)

@app.route('/static/lib/<path:filename>')
def serve_lib(filename):
    return send_from_directory('static/lib', filename)

@app.route('/static/scss/<path:filename>')
def serve_scss(filename):
    return send_from_directory('static/scss', filename)

@app.route('/static/css/<path:filename>')
def serve_css(filename):
    return send_from_directory('static/css', filename)

@app.before_request
def before_request():
    g.login = session.get('user_id', 0)
    g.app = app

@app.route('/logout')
def logout():
    session.clear()
    return redirect("/")

app.register_blueprint(news_blueprint, name='news_blueprint')
app.register_blueprint(users_blueprint, name='users_blueprint')
app.register_blueprint(authorization_blueprint, name='authorization_blueprint')
app.register_blueprint(search_blueprint, name='search_blueprint')
app.register_blueprint(categories_blueprint, name='categories_blueprint')
if __name__ == '__main__':
    app.run(debug=True)
