from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__= 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    address_id = db.Column(db.Integer, db.ForeignKey('addresses.id'))
    address = db.relationship('Addresses', backref='user', uselist=False) #devuelve un objeto                        


    def __repr__(self):
        return f'<User {self.email}>'

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "address" : self.address.serialize() if self.address else None
            # do not serialize the password, its a security breach
        }

#uno a uno
class Addresses(db.Model):
    __tablename__= 'addresses'
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(120), nullable=False)
    
    def __repr__(self):
        return f'<Address {self.id}>'

    def serialize(self):
        return {
            "id": self.id,
            "address": self.address,
            # do not serialize the password, its a security breach
        }
    
class Authors(db.Model):
    __tablename__= 'authors'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120), nullable=False)
    #uno a muchos
    books = db.relationship('Books', backref='author', lazy=True) # devuelve una lista



    def __repr__(self):
        return f'<Authors {self.full_name}>'

    def serialize(self):
        return {
            "id": self.id,
            "full_name": self.full_name,
            'books': [book.serialize() for book in self.books] if self.books else None
        }
    
#tabla secundaria para muchos a muchos
class Books_Categories(db.Model):
    __tablename__= 'books_categories'
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)

    def __repr__(self):
        return f'<Books_Categories {self.id}>'

    def serialize(self):
        return {
            "id": self.id,
            "book_id": self.book_id,
            'category_id': self.category_id
        }


class Books(db.Model):
    __tablename__= 'books'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    #uno a muchos
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'))
    categories = db.relationship('Books_Categories', backref='category', lazy=True) #devuelve lista

    def __repr__(self):
        return f'<Books {self.title}>'

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "categories" : [category.serialize() for category in self.categories] if self.categories else None
        }
    
class Categories(db.Model):
    __tablename__= 'categories'
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(120), nullable=False)
    books = db.relationship('Books_Categories', backref='book', lazy=True) #devuelve lista

    def __repr__(self):
        return f'<Categories {self.category}>'

    def serialize(self):
        return {
            "id": self.id,
            "category": self.category,
            "books" : [book.serialize() for book in self.books] if self.books else None

        }