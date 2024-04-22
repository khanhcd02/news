class Comment:
    def __init__(self, db_connection, comment_id=None, news_id=None, user_id=None, content=None, comment_at=None, rep_id=None, status=None):
        self.db_connection = db_connection
        self.id = comment_id
        self.news_id = news_id
        self.user_id = user_id
        self.content = content
        self.comment_at = comment_at
        self.rep_id = rep_id
        self.status = status

    def get_all_comments(self):
        return self.db_connection.CRUD("SELECT * FROM comments")

    def add_comment(self):
        self.db_connection.CRUD("INSERT INTO comments (NewsId, UserId, Content, CommentAt, RepId, Status) VALUES (%s, %s, %s, %s, %s, %s)", (self.news_id, self.user_id, self.content, self.comment_at, self.rep_id, self.status))

    def update_comment(self):
        self.db_connection.CRUD("UPDATE comments SET NewsId = %s, UserId = %s, Content = %s, CommentAt = %s, RepId = %s, Status = %s WHERE Id = %s", (self.news_id, self.user_id, self.content, self.comment_at, self.rep_id, self.status, self.id))

    def delete_comment(self):
        self.db_connection.CRUD("DELETE FROM comments WHERE Id = %s", (self.id,))


