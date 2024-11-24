from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Boolean,
    DateTime,
    ForeignKey,
    Text,
    Enum,
    create_engine,
    DECIMAL
)

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()  # Initialize the SQLAlchemy object

from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql import func
from sqlalchemy.ext.hybrid import hybrid_property
from werkzeug.security import generate_password_hash, check_password_hash

Base = declarative_base()


# Custom User Model
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(150), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)
    first_name = Column(String(30))
    last_name = Column(String(30))
    is_active = Column(Boolean, default=True)
    date_joined = Column(DateTime, server_default=func.now())

    @hybrid_property
    def password(self):
        raise AttributeError("Password is not readable.")

    @password.setter
    def password(self, raw_password):
        self.password_hash = generate_password_hash(raw_password)

    def verify_password(self, raw_password):
        return check_password_hash(self.password_hash, raw_password)

    def __repr__(self):
        return f"<User(username={self.username}, email={self.email})>"


# Base Product Model
class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_type = Column(Enum("book", "comic", "tshirt", name="product_types"), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    sku = Column(String(50), unique=True, nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    owner = relationship("User", back_populates="products")

    def __repr__(self):
        return f"<Product(name={self.name}, product_type={self.product_type})>"


User.products = relationship("Product", order_by=Product.id, back_populates="owner")


# Book Model
class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, ForeignKey("products.id"), primary_key=True)
    isbn = Column(String(13), unique=True, nullable=False)
    author = Column(String(255), nullable=False)
    page_count = Column(Integer, nullable=False)
    cover_type = Column(String(50), nullable=False)  # e.g., "hardcover" or "softcover"
    predefined_dimensions = Column(
        Enum(
            "6x9",
            "5.5x8.5",
            "7x10",
            "8.5x11",
            name="predefined_book_dimensions",
        ),
        nullable=True,
    )
    custom_width = Column(Float, nullable=True)
    custom_height = Column(Float, nullable=True)
    custom_depth = Column(Float, nullable=True)
    dimensions = Column(String(100), nullable=True)

    __mapper_args__ = {"polymorphic_identity": "book"}

    def save_dimensions(self):
        if self.predefined_dimensions:
            self.dimensions = dict(self.PREDEFINED_DIMENSIONS).get(self.predefined_dimensions)
        elif self.custom_width and self.custom_height:
            depth = f"x {self.custom_depth}" if self.custom_depth else ""
            self.dimensions = f"{self.custom_width} x {self.custom_height} {depth}".strip()

    def __repr__(self):
        return f"<Book(name={self.name}, isbn={self.isbn})>"


# Comic Book Model
class ComicBook(Base):
    __tablename__ = "comic_books"

    id = Column(Integer, ForeignKey("products.id"), primary_key=True)
    issue_number = Column(Integer, nullable=False)
    series_title = Column(String(255), nullable=False)
    predefined_dimensions = Column(
        Enum("6.625x10.25", "8.5x11", name="predefined_comic_dimensions"),
        nullable=True,
    )
    custom_width = Column(Float, nullable=True)
    custom_height = Column(Float, nullable=True)
    dimensions = Column(String(100), nullable=True)

    __mapper_args__ = {"polymorphic_identity": "comic"}

    def save_dimensions(self):
        if self.predefined_dimensions:
            self.dimensions = dict(self.PREDEFINED_DIMENSIONS).get(self.predefined_dimensions)
        elif self.custom_width and self.custom_height:
            self.dimensions = f"{self.custom_width} x {self.custom_height}".strip()

    def __repr__(self):
        return f"<ComicBook(name={self.name}, issue_number={self.issue_number})>"

# EBook Model
class EBook(Base):
    __tablename__ = "ebooks"

    id = Column(Integer, ForeignKey("products.id"), primary_key=True)
    author = Column(String(255), nullable=False)
    file_format = Column(
        Enum("PDF", "EPUB", "MOBI", name="ebook_formats"), nullable=False
    )
    file_size_mb = Column(Float, nullable=False, help_text="File size in megabytes")
    download_url = Column(String(500), nullable=False, help_text="URL to access the eBook")

    __mapper_args__ = {"polymorphic_identity": "ebook"}

    def __repr__(self):
        return f"<EBook(name={self.name}, author={self.author}, format={self.file_format})>"


# T-Shirt Model
class TShirt(Base):
    __tablename__ = "tshirts"

    id = Column(Integer, ForeignKey("products.id"), primary_key=True)
    size = Column(String(10), nullable=False)  # e.g., "S", "M", "L", "XL", "XXL", "XXXL"
    color = Column(String(50), nullable=False)
    material = Column(String(100), nullable=False)  # e.g., "Cotton", "Polyester"

    __mapper_args__ = {"polymorphic_identity": "tshirt"}

    def __repr__(self):
        return f"<TShirt(name={self.name}, size={self.size}, color={self.color})>"


# Setup the database engine
# Replace 'sqlite:///app.db' with your database connection string
engine = create_engine("sqlite:///app.db")

# Create all tables
Base.metadata.create_all(engine)
