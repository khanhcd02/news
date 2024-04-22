class Bookmark:
    def __init__(self, db_connection, bookmark_id=None, user_id=None, news_id=None):
        self.db_connection = db_connection
        self.id = bookmark_id
        self.user_id = user_id
        self.news_id = news_id

    def get_all_bookmarks(self):
        return self.db_connection.CRUD("SELECT * FROM bookmarks")

    def add_bookmark(self):
        self.db_connection.CRUD("INSERT INTO bookmarks (UserId, NewsId) VALUES (%s, %s)", (self.user_id, self.news_id))

    def delete_bookmark(self):
        self.db_connection.CRUD("DELETE FROM bookmarks WHERE Id = %s", (self.id,))

