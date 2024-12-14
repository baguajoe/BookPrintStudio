from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

# User Model
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())

    orders = db.relationship("Order", back_populates="customer", cascade="all, delete")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }


# Base Product Model
class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_type = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    sku = db.Column(db.String(50), unique=True, nullable=False)
    price = db.Column(db.DECIMAL(10, 2), nullable=False)
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())

    pricing = db.relationship("Pricing", back_populates="product", uselist=False)

    __mapper_args__ = {"polymorphic_on": product_type, "polymorphic_identity": "product"}

    def to_dict(self):
        return {
            "id": self.id,
            "product_type": self.product_type,
            "name": self.name,
            "description": self.description,
            "sku": self.sku,
            "price": str(self.price),
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }


# Specialized Product Models
class Book(Product):
    __tablename__ = "books"

    id = db.Column(db.Integer, db.ForeignKey("products.id"), primary_key=True)
    isbn = db.Column(db.String(13), unique=True, nullable=False)
    author = db.Column(db.String(255), nullable=False)
    page_count = db.Column(db.Integer, nullable=False)
    cover_type = db.Column(db.String(50), nullable=False)
    trim_size = db.Column(db.String(50), nullable=False)
    paper_type = db.Column(db.String(50), nullable=False)

    __mapper_args__ = {"polymorphic_identity": "book"}

    def to_dict(self):
        base_dict = super().to_dict()
        book_dict = {
            "isbn": self.isbn,
            "author": self.author,
            "page_count": self.page_count,
            "cover_type": self.cover_type,
            "trim_size": self.trim_size,
            "paper_type": self.paper_type,
        }
        return {**base_dict, **book_dict}


class ComicBook(Product):
    __tablename__ = "comic_books"

    id = db.Column(db.Integer, db.ForeignKey("products.id"), primary_key=True)
    issue_number = db.Column(db.Integer, nullable=False)
    series_title = db.Column(db.String(255), nullable=False)
    cover_type = db.Column(db.String(50), nullable=True)
    trim_size = db.Column(db.String(50), nullable=False)
    page_count = db.Column(db.Integer, nullable=False)

    __mapper_args__ = {"polymorphic_identity": "comic_book"}

    def to_dict(self):
        base_dict = super().to_dict()
        comic_dict = {
            "issue_number": self.issue_number,
            "series_title": self.series_title,
            "cover_type": self.cover_type,
            "trim_size": self.trim_size,
            "page_count": self.page_count,
        }
        return {**base_dict, **comic_dict}


class TShirt(Product):
    __tablename__ = "tshirts"

    id = db.Column(db.Integer, db.ForeignKey("products.id"), primary_key=True)
    size = db.Column(db.String(10), nullable=False)
    color = db.Column(db.String(50), nullable=False)
    material = db.Column(db.String(100), nullable=False)

    __mapper_args__ = {"polymorphic_identity": "tshirt"}

    def to_dict(self):
        base_dict = super().to_dict()
        tshirt_dict = {
            "size": self.size,
            "color": self.color,
            "material": self.material,
        }
        return {**base_dict, **tshirt_dict}


class EBook(Product):
    __tablename__ = "ebooks"

    id = db.Column(db.Integer, db.ForeignKey("products.id"), primary_key=True)
    file_format = db.Column(db.String(20), nullable=False)
    download_url = db.Column(db.String(255), nullable=False)
    file_size = db.Column(db.String(50), nullable=True)

    __mapper_args__ = {"polymorphic_identity": "ebook"}

    def to_dict(self):
        base_dict = super().to_dict()
        ebook_dict = {
            "file_format": self.file_format,
            "download_url": self.download_url,
            "file_size": self.file_size,
        }
        return {**base_dict, **ebook_dict}


# Order Model
class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    total_price = db.Column(db.DECIMAL(10, 2), nullable=False)
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())

    customer = db.relationship("User", back_populates="orders")

    def to_dict(self):
        return {
            "id": self.id,
            "customer_id": self.customer_id,
            "status": self.status,
            "total_price": str(self.total_price),
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }


# Pricing Model
class Pricing(db.Model):
    __tablename__ = "pricing"

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    base_price = db.Column(db.DECIMAL(10, 2), nullable=False)
    discount = db.Column(db.DECIMAL(5, 2), default=0.0)
    tax_rate = db.Column(db.DECIMAL(5, 2), default=0.0)
    final_price = db.Column(db.DECIMAL(10, 2), nullable=False)
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())

    product = db.relationship("Product", back_populates="pricing")

    def calculate_final_price(self):
        self.final_price = self.base_price * (1 - self.discount) * (1 + self.tax_rate)

    def to_dict(self):
        return {
            "id": self.id,
            "product_id": self.product_id,
            "base_price": str(self.base_price),
            "discount": str(self.discount),
            "tax_rate": str(self.tax_rate),
            "final_price": str(self.final_price),
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
    
class ChildrenBook(Book):
    __tablename__ = "children_books"

    id = db.Column(db.Integer, db.ForeignKey("books.id"), primary_key=True)
    age_group = db.Column(db.String(50), nullable=False)
    illustration_style = db.Column(db.String(100), nullable=False)

    __mapper_args__ = {"polymorphic_identity": "children_book"}

    def to_dict(self):
        base_dict = super().to_dict()
        children_dict = {
            "age_group": self.age_group,
            "illustration_style": self.illustration_style,
        }
        return {**base_dict, **children_dict}

