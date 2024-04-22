class Category:
    def __init__(self, db_connection, category_id=None, category_name=None, parent_id=None, status=None):
        self.db_connection = db_connection
        self.id = category_id
        self.name = category_name
        self.parent_id = parent_id
        self.status = status

    def get_all_categories(self):
        return self.db_connection.CRUD("SELECT c1.Id AS Id, c1.CategoryName AS CategoryName, c1.Status, c2.Id AS ParentId, c2.CategoryName AS ParentName FROM categories c1 LEFT JOIN categories c2 ON c1.ParentId = c2.Id")

    def get_category_by_id(self, category_id):
        return self.db_connection.CRUD("SELECT * FROM categories WHERE Id = %s", (category_id,))

    def add_category(self):
        self.db_connection.CRUD("INSERT INTO categories (CategoryName, ParentId, Status) VALUES (%s, %s, %s)", (self.name, self.parent_id, self.status))

    def update_category(self):
        self.db_connection.CRUD("UPDATE categories SET CategoryName = %s, ParentId = %s, Status = %s WHERE Id = %s", (self.name, self.parent_id, self.status, self.id))
