from flask import Blueprint, jsonify, request
from .models import db, User, Product, Book, ComicBook, ChildrenBook, EBook, TShirt, Pricing

api = Blueprint("api", __name__)
pricing_api = Blueprint("pricing_api", __name__)

# -------------------- User Routes --------------------

@api.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users]), 200

@api.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict()), 200

@api.route("/users", methods=["POST"])
def create_user():
    data = request.json
    try:
        user = User(
            username=data["username"],
            email=data["email"],
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
        )
        user.set_password(data["password"])
        db.session.add(user)
        db.session.commit()
        return jsonify({"message": "User created successfully!", "user": user.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error creating user: {str(e)}"}), 400

@api.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.json
    try:
        for key, value in data.items():
            if hasattr(user, key):
                setattr(user, key, value)
        db.session.commit()
        return jsonify({"message": "User updated successfully!", "user": user.to_dict()}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error updating user: {str(e)}"}), 400

@api.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    try:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User deleted successfully!"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error deleting user: {str(e)}"}), 400


# -------------------- Product Routes --------------------

@api.route("/products", methods=["GET"])
def get_products():
    product_type = request.args.get("type")
    if product_type:
        products = Product.query.filter_by(product_type=product_type).all()
    else:
        products = Product.query.all()
    return jsonify([product.to_dict() for product in products]), 200

@api.route("/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    product = Product.query.get_or_404(product_id)
    return jsonify(product.to_dict()), 200

@api.route("/products", methods=["POST"])
def create_product():
    data = request.json
    product_type = data.pop("product_type", "product")

    model_map = {
        "book": Book,
        "comic_book": ComicBook,
        "children_book": ChildrenBook,
        "tshirt": TShirt,
        "ebook": EBook,
        "product": Product,
    }

    try:
        if product_type not in model_map:
            return jsonify({"error": "Invalid product type"}), 400

        product = model_map[product_type](**data)
        db.session.add(product)
        db.session.commit()
        return jsonify({"message": f"{product_type.title()} created successfully!", "product": product.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error creating product: {str(e)}"}), 400

@api.route("/products/<int:product_id>", methods=["PUT"])
def update_product(product_id):
    product = Product.query.get_or_404(product_id)
    data = request.json
    try:
        for key, value in data.items():
            if hasattr(product, key):
                setattr(product, key, value)
        db.session.commit()
        return jsonify({"message": "Product updated successfully!", "product": product.to_dict()}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error updating product: {str(e)}"}), 400

@api.route("/products/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    try:
        db.session.delete(product)
        db.session.commit()
        return jsonify({"message": "Product deleted successfully!"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error deleting product: {str(e)}"}), 400


# -------------------- Pricing Routes --------------------

@pricing_api.route("/pricing", methods=["GET"])
def get_pricing():
    pricing_records = Pricing.query.all()
    return jsonify([pricing.to_dict() for pricing in pricing_records]), 200

@pricing_api.route("/pricing/<int:product_id>", methods=["GET"])
def get_product_pricing(product_id):
    pricing = Pricing.query.filter_by(product_id=product_id).first_or_404()
    return jsonify(pricing.to_dict()), 200

@pricing_api.route("/pricing", methods=["POST"])
def create_or_update_pricing():
    data = request.json
    try:
        product_id = data["product_id"]
        pricing = Pricing.query.filter_by(product_id=product_id).first()

        if not pricing:
            pricing = Pricing(product_id=product_id)

        pricing.base_price = data["base_price"]
        pricing.discount = data.get("discount", 0.0)
        pricing.tax_rate = data.get("tax_rate", 0.0)
        pricing.calculate_final_price()

        db.session.add(pricing)
        db.session.commit()
        return jsonify({"message": "Pricing created/updated successfully!", "pricing": pricing.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error updating pricing: {str(e)}"}), 400

@pricing_api.route("/pricing/<int:product_id>", methods=["DELETE"])
def delete_pricing(product_id):
    pricing = Pricing.query.filter_by(product_id=product_id).first_or_404()
    try:
        db.session.delete(pricing)
        db.session.commit()
        return jsonify({"message": "Pricing deleted successfully!"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error deleting pricing: {str(e)}"}), 400


# -------------------- Utility Routes --------------------

@api.route("/standard_specifications/<product_type>", methods=["GET"])
def get_standard_specifications(product_type):
    try:
        products = Product.query.filter_by(product_type=product_type).all()
        return jsonify([product.to_dict() for product in products]), 200
    except Exception as e:
        return jsonify({"error": f"Error fetching specifications: {str(e)}"}), 400
