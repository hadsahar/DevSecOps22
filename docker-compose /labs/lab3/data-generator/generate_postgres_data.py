#!/usr/bin/env python3
"""
PostgreSQL Data Generator
Generates random sample data for PostgreSQL database
"""

import random
import string
from datetime import datetime, timedelta
import psycopg2
from psycopg2 import sql
from faker import Faker
import json

# Initialize Faker
fake = Faker()

# PostgreSQL connection settings
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "appdb"
DB_USER = "appuser"
DB_PASSWORD = "apppassword123"

def generate_random_string(length=10):
    """Generate random string"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def get_db_connection():
    """Create database connection"""
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None

def generate_users(count=100):
    """Generate random user records"""
    users = []
    for _ in range(count):
        user = {
            'username': fake.user_name(),
            'email': fake.email(),
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'age': random.randint(18, 80),
            'city': fake.city(),
            'country': fake.country(),
            'bio': fake.text(max_nb_chars=200),
            'is_active': random.choice([True, False]),
            'registration_date': fake.date_time_between(start_date='-2y', end_date='now'),
            'last_login': fake.date_time_between(start_date='-30d', end_date='now')
        }
        users.append(user)
    return users

def generate_products(count=200):
    """Generate random product records"""
    categories = ["Electronics", "Clothing", "Books", "Home & Garden", "Sports", "Toys", "Food", "Beauty", "Automotive", "Health"]
    products = []
    
    for i in range(count):
        dimensions = {
            'length': round(random.uniform(5.0, 100.0), 2),
            'width': round(random.uniform(5.0, 100.0), 2),
            'height': round(random.uniform(5.0, 100.0), 2)
        }
        
        images = [
            f"https://picsum.photos/seed/{generate_random_string(10)}/400/300.jpg",
            f"https://picsum.photos/seed/{generate_random_string(10)}/400/300.jpg"
        ]
        
        tags = random.sample(["popular", "sale", "new", "limited", "eco-friendly", "premium", "bestseller", "trending"], k=random.randint(1, 3))
        
        product = {
            'product_id': f"PROD-{str(i+1).zfill(6)}",
            'name': fake.catch_phrase(),
            'description': fake.text(max_nb_chars=500),
            'category': random.choice(categories),
            'price': round(random.uniform(10.0, 999.99), 2),
            'currency': 'USD',
            'stock': random.randint(0, 1000),
            'sku': f"SKU-{generate_random_string(8).upper()}",
            'brand': fake.company(),
            'weight': round(random.uniform(0.1, 50.0), 2),
            'dimensions': json.dumps(dimensions),
            'images': json.dumps(images),
            'tags': tags,
            'rating': round(random.uniform(1.0, 5.0), 1),
            'reviews': random.randint(0, 500),
            'is_active': random.choice([True, False])
        }
        products.append(product)
    return products

def generate_orders(count=300, user_ids=None, product_ids=None):
    """Generate random order records"""
    if user_ids is None:
        user_ids = list(range(1, 101))
    if product_ids is None:
        product_ids = list(range(1, 201))
    
    orders = []
    statuses = ["pending", "processing", "shipped", "delivered", "cancelled"]
    
    for i in range(count):
        shipping_address = {
            'street': fake.street_address(),
            'city': fake.city(),
            'state': fake.state(),
            'zip_code': fake.zipcode(),
            'country': fake.country()
        }
        
        order = {
            'order_id': f"ORD-{str(i+1).zfill(8)}",
            'user_id': random.choice(user_ids),
            'total_amount': round(random.uniform(20.0, 2000.0), 2),
            'currency': 'USD',
            'status': random.choice(statuses),
            'shipping_address': json.dumps(shipping_address),
            'payment_method': random.choice(["credit_card", "paypal", "bank_transfer", "crypto"]),
            'order_date': fake.date_time_between(start_date='-6m', end_date='now'),
            'shipping_date': fake.date_time_between(start_date='-5m', end_date='now') if random.random() > 0.3 else None,
            'delivery_date': fake.date_time_between(start_date='-4m', end_date='now') if random.random() > 0.5 else None
        }
        orders.append(order)
    return orders

def generate_order_items(orders, product_ids):
    """Generate order items for orders"""
    order_items = []
    
    for order in orders:
        num_items = random.randint(1, 4)
        for _ in range(num_items):
            order_item = {
                'order_id': order['id'],  # Will be updated after insertion
                'product_id': random.choice(product_ids),
                'quantity': random.randint(1, 5),
                'price': round(random.uniform(10.0, 999.99), 2)
            }
            order_items.append(order_item)
    
    return order_items

def insert_users(conn, users):
    """Insert users into database"""
    cursor = conn.cursor()
    
    insert_query = sql.SQL("""
        INSERT INTO app_schema.users (username, email, first_name, last_name, age, city, country, bio, is_active, registration_date, last_login)
        VALUES (%(username)s, %(email)s, %(first_name)s, %(last_name)s, %(age)s, %(city)s, %(country)s, %(bio)s, %(is_active)s, %(registration_date)s, %(last_login)s)
        RETURNING id
    """)
    
    user_ids = []
    for user in users:
        try:
            cursor.execute(insert_query, user)
            user_id = cursor.fetchone()[0]
            user_ids.append(user_id)
        except Exception as e:
            print(f"Error inserting user {user['username']}: {e}")
            continue
    
    conn.commit()
    cursor.close()
    return user_ids

def insert_products(conn, products):
    """Insert products into database"""
    cursor = conn.cursor()
    
    insert_query = sql.SQL("""
        INSERT INTO app_schema.products (product_id, name, description, category, price, currency, stock, sku, brand, weight, dimensions, images, tags, rating, reviews, is_active)
        VALUES (%(product_id)s, %(name)s, %(description)s, %(category)s, %(price)s, %(currency)s, %(stock)s, %(sku)s, %(brand)s, %(weight)s, %(dimensions)s, %(images)s, %(tags)s, %(rating)s, %(reviews)s, %(is_active)s)
        RETURNING id
    """)
    
    product_ids = []
    for product in products:
        try:
            cursor.execute(insert_query, product)
            product_id = cursor.fetchone()[0]
            product_ids.append(product_id)
        except Exception as e:
            print(f"Error inserting product {product['product_id']}: {e}")
            continue
    
    conn.commit()
    cursor.close()
    return product_ids

def insert_orders(conn, orders):
    """Insert orders into database"""
    cursor = conn.cursor()
    
    insert_query = sql.SQL("""
        INSERT INTO app_schema.orders (order_id, user_id, total_amount, currency, status, shipping_address, payment_method, order_date, shipping_date, delivery_date)
        VALUES (%(order_id)s, %(user_id)s, %(total_amount)s, %(currency)s, %(status)s, %(shipping_address)s, %(payment_method)s, %(order_date)s, %(shipping_date)s, %(delivery_date)s)
        RETURNING id
    """)
    
    order_ids = []
    for order in orders:
        try:
            cursor.execute(insert_query, order)
            order_id = cursor.fetchone()[0]
            order['id'] = order_id  # Store the ID for order items
            order_ids.append(order_id)
        except Exception as e:
            print(f"Error inserting order {order['order_id']}: {e}")
            continue
    
    conn.commit()
    cursor.close()
    return order_ids

def insert_order_items(conn, order_items):
    """Insert order items into database"""
    cursor = conn.cursor()
    
    insert_query = sql.SQL("""
        INSERT INTO app_schema.order_items (order_id, product_id, quantity, price)
        VALUES (%(order_id)s, %(product_id)s, %(quantity)s, %(price)s)
    """)
    
    for item in order_items:
        try:
            cursor.execute(insert_query, item)
        except Exception as e:
            print(f"Error inserting order item: {e}")
            continue
    
    conn.commit()
    cursor.close()

def main():
    """Main function to generate and insert data"""
    conn = None
    try:
        print("Connecting to PostgreSQL database...")
        conn = get_db_connection()
        
        if conn is None:
            print("Failed to connect to database")
            return
        
        print("Connected to database successfully!")
        
        # Clear existing data
        print("Clearing existing data...")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM app_schema.order_items")
        cursor.execute("DELETE FROM app_schema.orders")
        cursor.execute("DELETE FROM app_schema.products")
        cursor.execute("DELETE FROM app_schema.users")
        conn.commit()
        cursor.close()
        
        # Generate and insert users
        print("Generating and inserting users...")
        users = generate_users(100)
        user_ids = insert_users(conn, users)
        print(f"Inserted {len(user_ids)} users")
        
        # Generate and insert products
        print("Generating and inserting products...")
        products = generate_products(200)
        product_ids = insert_products(conn, products)
        print(f"Inserted {len(product_ids)} products")
        
        # Generate and insert orders
        print("Generating and inserting orders...")
        orders = generate_orders(300, user_ids, product_ids)
        order_ids = insert_orders(conn, orders)
        print(f"Inserted {len(order_ids)} orders")
        
        # Generate and insert order items
        print("Generating and inserting order items...")
        order_items = generate_order_items(orders, product_ids)
        insert_order_items(conn, order_items)
        print(f"Inserted {len(order_items)} order items")
        
        # Display statistics
        print("\n=== Database Statistics ===")
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM app_schema.users")
        user_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM app_schema.products")
        product_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM app_schema.orders")
        order_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM app_schema.order_items")
        order_item_count = cursor.fetchone()[0]
        
        print(f"Users: {user_count}")
        print(f"Products: {product_count}")
        print(f"Orders: {order_count}")
        print(f"Order Items: {order_item_count}")
        
        cursor.close()
        
        print("\nData generation completed successfully!")
        
    except Exception as e:
        print(f"Error: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    main()
