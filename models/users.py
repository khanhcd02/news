class User:
    def __init__(self, db_connection, user_id=None, name=None, image=None, username=None, password=None, email=None, birth_day=None, phone_number=None, address=None, status=None):
        self.db_connection = db_connection
        self.id = user_id
        self.name = name
        self.image = image
        self.username = username
        self.password = password
        self.email = email
        self.birth_day = birth_day
        self.phone_number = phone_number
        self.address = address
        self.status = status

    def get_all_users(self):
        return self.db_connection.CRUD("SELECT * FROM users")

    def get_user_by_id(self,id):
        return self.db_connection.CRUD("SELECT * FROM users WHERE Id = %s", (id,))

    def register(self):
        self.db_connection.CRUD("INSERT INTO users (Name, Image, Username, Password, Email, BirthDay, PhoneNumber, Address, Status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", (self.name, self.image, self.username, self.password, self.email, self.birth_day, self.phone_number, self.address, 1))
        # return self.db_connection.CRUD("SELECT LAST_INSERT_ID() as Id")
    
    def update_user(self):
        self.db_connection.CRUD("UPDATE users SET Name = %s, Image = %s, Password = %s, Email = %s, BirthDay = %s, PhoneNumber = %s, Address = %s, Status = %s WHERE Id = %s", (self.name, self.image, self.password, self.email, self.birth_day, self.phone_number, self.address, self.status, self.id))

    def login(self):
        return self.db_connection.CRUD("SELECT * FROM users WHERE Username = %s AND Password = %s",(self.username,self.password))

    def check_username(self):
        return self.db_connection.CRUD("SELECT * FROM users WHERE Username = %s",(self.username,))
    
    def get_author_by_keyword(self, keyword):
        return self.db_connection.CRUD("SELECT users.Id, users.Name, users.Image FROM users JOIN news ON news.AuthorId = users.Id JOIN categories ON news.CategoryId = Categories.Id WHERE (users.Status='1') AND (news.Title LIKE %s OR news.Content LIKE %s OR categories.CategoryName LIKE %s OR users.Name LIKE %s) GROUP BY users.Id", (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"))

    