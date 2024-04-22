class Authorization:
    def __init__(self, db_connection, auth_id=None, user_id=None, manage_news=None, manage_users=None, manage_bookmarks=None, manage_categories=None, manage_comments=None, manage_authorization=None):
        self.db_connection = db_connection
        self.id = auth_id
        self.user_id = user_id
        self.manage_news = manage_news
        self.manage_users = manage_users
        self.manage_bookmarks = manage_bookmarks
        self.manage_categories = manage_categories
        self.manage_comments = manage_comments
        self.manage_authorization = manage_authorization

    def get_all_authorizations(self):
        return self.db_connection.CRUD("SELECT authorization.*, users.Name FROM newsdb.authorization JOIN users ON authorization.UserId = users.Id")
   
    def add_authorization(self):
        self.db_connection.CRUD("INSERT INTO authorization (UserId, ManageNews, ManageUsers, ManageBookmarks, ManageCategories, ManageComments, ManageAuthorization) VALUES (%s, %s, %s, %s, %s, %s, %s)", (self.user_id, self.manage_news, self.manage_users, self.manage_bookmarks, self.manage_categories, self.manage_comments, self.manage_authorization))

    def update_authorization(self):
        self.db_connection.CRUD("UPDATE authorization SET ManageNews = %s, ManageUsers = %s, ManageBookmarks = %s, ManageCategories = %s, ManageComments = %s , ManageAuthorization = %s WHERE UserId = %s", (self.manage_news, self.manage_users, self.manage_bookmarks, self.manage_categories, self.manage_comments, self.manage_authorization, self.user_id))

    def check_access(self,user_id):
        return self.db_connection.CRUD("SELECT authorization.*, users.Name FROM newsdb.authorization JOIN users ON authorization.UserId = users.Id where UserId=%s", (user_id,))

    def list_user_need_permission(self):
        return self.db_connection.CRUD("SELECT Id,Name FROM users WHERE Status = '1' and Id NOT IN (SELECT UserId FROM authorization);")