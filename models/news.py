from models.dbconnect import DatabaseConnection
class News:
    def __init__(self,db_connection, news_id=None, title=None, content=None, image=None, author_id=None, published_at=None, category_id=None, status=None):
        self.db_connection = db_connection
        self.id = news_id
        self.title = title
        self.content = content
        self.image = image
        self.author_id = author_id
        self.published_at = published_at
        self.category_id = category_id
        self.status = status

    def get_all_news(self):
        return self.db_connection.CRUD("SELECT news.Id,news.Title,news.Image,news.PublishedAt,news.Status,users.Name as Author,CategoryName,users.Image as userImg FROM news join users,categories WHERE users.Id = news.AuthorId and categories.Id = news.CategoryId order by PublishedAt desc;")
    
    def get_hot_news(self):
        return self.db_connection.CRUD("SELECT news.Id,news.Title,news.Image,news.PublishedAt,news.AuthorId,users.Name as Author,CategoryName,users.Image as userImg FROM news join users,categories WHERE users.Id = news.AuthorId and categories.Id = news.CategoryId and news.Status ='1' ORDER BY PublishedAt DESC limit 20")

    def get_news_by_id(self,id):
        return self.db_connection.CRUD("SELECT news.*,users.Name as Author,CategoryName,ParentId,users.Image as userImg FROM news join users,categories WHERE news.Id = %s and users.Id = news.AuthorId and categories.Id = news.CategoryId", (id,))
    
    def get_news_by_category_id(self,id):
        return self.db_connection.CRUD("SELECT news.Id,news.Title,news.Image,news.PublishedAt,news.AuthorId,users.Name as Author,CategoryName,ParentId,users.Image as userImg FROM news join users,categories WHERE news.Status = '1' and news.CategoryId = %s and users.Id = news.AuthorId and categories.Id = news.CategoryId order by PublishedAt desc", (id,))

    def get_news_by_author_id(self,id):
        return self.db_connection.CRUD("SELECT news.Id,news.Title,news.Image,news.PublishedAt,news.AuthorId,users.Name as Author,CategoryName,ParentId,users.Image as userImg FROM news join users,categories WHERE news.Status = '1' and news.AuthorId = %s and users.Id = news.AuthorId and categories.Id = news.CategoryId order by PublishedAt desc", (id,))

    def add_news(self):
        self.db_connection.CRUD("INSERT INTO news (Title, Content, Image, AuthorId, PublishedAt, CategoryId, Status) VALUES (%s, %s, %s, %s, %s, %s, %s)", (self.title, self.content, self.image, self.author_id, self.published_at, self.category_id, self.status))

    def update_news(self):
        self.db_connection.CRUD("UPDATE news SET Title = %s, Content = %s, Image = %s, PublishedAt = %s, CategoryId = %s, Status = %s WHERE Id = %s", (self.title, self.content, self.image, self.published_at, self.category_id, self.status, self.id))

    def get_news_by_keyword(self, keyword):
        return self.db_connection.CRUD("SELECT news.Id, news.Title, news.Image, news.PublishedAt, CategoryName, CategoryId, users.Name AS Author, users.Image AS userImg FROM news JOIN categories ON news.CategoryId = Categories.Id JOIN users ON news.AuthorId = users.Id WHERE (news.Status='1') AND (news.Title LIKE %s OR news.Content LIKE %s OR categories.CategoryName LIKE %s OR users.Name LIKE %s) ORDER BY PublishedAt DESC;", (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"))

        

    