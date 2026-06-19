#!/usr/bin/env python3
"""
Flask Backend Application
RESTful API for the full-stack application
"""

import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from marshmallow import Schema, fields
from datetime import datetime
import logging

# Initialize Flask app
app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://appuser:apppassword123@postgres:5432/appdb')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-here')

# Initialize extensions
db = SQLAlchemy(app)
ma = Marshmallow(app)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import models (we'll define them inline for simplicity)
class User(db.Model):
    __tablename__ = 'users'
    __table_args__ = {'schema': 'app_schema'}
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    age = db.Column(db.Integer)
    city = db.Column(db.String(100))
    country = db.Column(db.String(100))
    bio = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    registration_date = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Product(db.Model):
    __tablename__ = 'products'
    __table_args__ = {'schema': 'app_schema'}
    
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(50))
    price = db.Column(db.Numeric(10, 2))
    currency = db.Column(db.String(3), default='USD')
    stock = db.Column(db.Integer, default=0)
    sku = db.Column(db.String(50), unique=True)
    brand = db.Column(db.String(100))
    weight = db.Column(db.Numeric(8, 2))
    dimensions = db.Column(db.JSON)
    images = db.Column(db.JSON)
    tags = db.Column(db.ARRAY(db.Text))
    rating = db.Column(db.Numeric(2, 1))
    reviews = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Order(db.Model):
    __tablename__ = 'orders'
    __table_args__ = {'schema': 'app_schema'}
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.String(20), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('app_schema.users.id'))
    total_amount = db.Column(db.Numeric(10, 2))
    currency = db.Column(db.String(3), default='USD')
    status = db.Column(db.String(20), default='pending')
    shipping_address = db.Column(db.JSON)
    payment_method = db.Column(db.String(50))
    order_date = db.Column(db.DateTime, default=datetime.utcnow)
    shipping_date = db.Column(db.DateTime)
    delivery_date = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Marshmallow schemas
class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_fk = True

class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Product

class OrderSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Order
        include_fk = True

# Initialize schemas
user_schema = UserSchema()
users_schema = UserSchema(many=True)
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)
order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)

# Routes
@app.route('/')
def index():
    return jsonify({
        'message': 'Flask Backend API',
        'version': '1.0.0',
        'status': 'running',
        'timestamp': datetime.utcnow().isoformat()
    })

@app.route('/health')
def health_check():
    try:
        # Test database connection
        db.session.execute('SELECT 1')
        return jsonify({
            'status': 'healthy',
            'database': 'connected',
            'timestamp': datetime.utcnow().isoformat()
        })
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'database': 'disconnected',
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }), 500

@app.route('/api/users', methods=['GET'])
def get_users():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        users = User.query.paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'users': users_schema.dump(users.items),
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': users.total,
                'pages': users.pages
            }
        })
    except Exception as e:
        logger.error(f"Error getting users: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    try:
        user = User.query.get_or_404(user_id)
        return jsonify(user_schema.dump(user))
    except Exception as e:
        logger.error(f"Error getting user {user_id}: {e}")
        return jsonify({'error': 'User not found'}), 404

@app.route('/api/products', methods=['GET'])
def get_products():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        category = request.args.get('category')
        
        query = Product.query
        if category:
            query = query.filter(Product.category == category)
        
        products = query.paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'products': products_schema.dump(products.items),
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': products.total,
                'pages': products.pages
            }
        })
    except Exception as e:
        logger.error(f"Error getting products: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    try:
        product = Product.query.get_or_404(product_id)
        return jsonify(product_schema.dump(product))
    except Exception as e:
        logger.error(f"Error getting product {product_id}: {e}")
        return jsonify({'error': 'Product not found'}), 404

@app.route('/api/orders', methods=['GET'])
def get_orders():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        user_id = request.args.get('user_id', type=int)
        
        query = Order.query
        if user_id:
            query = query.filter(Order.user_id == user_id)
        
        orders = query.paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'orders': orders_schema.dump(orders.items),
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': orders.total,
                'pages': orders.pages
            }
        })
    except Exception as e:
        logger.error(f"Error getting orders: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/orders', methods=['POST'])
def create_order():
    try:
        data = request.get_json()
        
        # Create new order
        order = Order(
            order_id=f"ORD-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
            user_id=data.get('user_id'),
            total_amount=data.get('total_amount'),
            status='pending',
            shipping_address=data.get('shipping_address'),
            payment_method=data.get('payment_method')
        )
        
        db.session.add(order)
        db.session.commit()
        
        return jsonify(order_schema.dump(order)), 201
    except Exception as e:
        logger.error(f"Error creating order: {e}")
        db.session.rollback()
        return jsonify({'error': 'Failed to create order'}), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    try:
        user_count = User.query.count()
        product_count = Product.query.count()
        order_count = Order.query.count()
        
        return jsonify({
            'users': user_count,
            'products': product_count,
            'orders': order_count,
            'timestamp': datetime.utcnow().isoformat()
        })
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        return jsonify({'error': 'Internal server error'}), 500

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Resource not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

# Initialize database
@app.before_first_request
def create_tables():
    db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
