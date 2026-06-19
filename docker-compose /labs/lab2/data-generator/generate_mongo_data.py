#!/usr/bin/env python3
"""
MongoDB Data Generator
Generates random sample data for MongoDB collections
"""

import random
import string
from datetime import datetime, timedelta
from pymongo import MongoClient
from faker import Faker

# Initialize Faker
fake = Faker()

# MongoDB connection settings
MONGO_URI = "mongodb://admin:securepassword123@localhost:27017/"
DATABASE_NAME = "testdb"

def generate_random_string(length=10):
    """Generate random string"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def generate_users(count=50):
    """Generate random user documents"""
    users = []
    for _ in range(count):
        user = {
            "username": fake.user_name(),
            "email": fake.email(),
            "firstName": fake.first_name(),
            "lastName": fake.last_name(),
            "age": random.randint(18, 80),
            "city": fake.city(),
            "country": fake.country(),
            "bio": fake.text(max_nb_chars=200),
            "isActive": random.choice([True, False]),
            "registrationDate": fake.date_time_between(start_date='-2y', end_date='now'),
            "lastLogin": fake.date_time_between(start_date='-30d', end_date='now'),
            "profile": {
                "avatar": f"https://picsum.photos/seed/{generate_random_string(10)}/200/200.jpg",
                "website": fake.url(),
                "social": {
                    "twitter": f"@{fake.user_name()}",
                    "linkedin": fake.url()
                }
            },
            "preferences": {
                "theme": random.choice(["light", "dark"]),
                "language": random.choice(["en", "es", "fr", "de", "it"]),
                "notifications": random.choice([True, False])
            }
        }
        users.append(user)
    return users

def generate_products(count=100):
    """Generate random product documents"""
    categories = ["Electronics", "Clothing", "Books", "Home & Garden", "Sports", "Toys", "Food", "Beauty"]
    products = []
    
    for i in range(count):
        product = {
            "productId": f"PROD-{str(i+1).zfill(6)}",
            "name": fake.catch_phrase(),
            "description": fake.text(max_nb_chars=500),
            "category": random.choice(categories),
            "price": round(random.uniform(10.0, 999.99), 2),
            "currency": "USD",
            "stock": random.randint(0, 1000),
            "sku": f"SKU-{generate_random_string(8).upper()}",
            "brand": fake.company(),
            "weight": round(random.uniform(0.1, 50.0), 2),
            "dimensions": {
                "length": round(random.uniform(5.0, 100.0), 2),
                "width": round(random.uniform(5.0, 100.0), 2),
                "height": round(random.uniform(5.0, 100.0), 2)
            },
            "images": [
                f"https://picsum.photos/seed/{generate_random_string(10)}/400/300.jpg",
                f"https://picsum.photos/seed/{generate_random_string(10)}/400/300.jpg"
            ],
            "tags": random.sample(["popular", "sale", "new", "limited", "eco-friendly", "premium"], k=random.randint(1, 3)),
            "rating": round(random.uniform(1.0, 5.0), 1),
            "reviews": random.randint(0, 500),
            "createdAt": fake.date_time_between(start_date='-1y', end_date='now'),
            "updatedAt": fake.date_time_between(start_date='-30d', end_date='now'),
            "isActive": random.choice([True, False])
        }
        products.append(product)
    return products

def generate_orders(count=200):
    """Generate random order documents"""
    orders = []
    statuses = ["pending", "processing", "shipped", "delivered", "cancelled"]
    
    for i in range(count):
        order = {
            "orderId": f"ORD-{str(i+1).zfill(8)}",
            "userId": random.randint(1, 50),
            "items": [
                {
                    "productId": f"PROD-{str(random.randint(1, 100)).zfill(6)}",
                    "quantity": random.randint(1, 5),
                    "price": round(random.uniform(10.0, 999.99), 2)
                }
                for _ in range(random.randint(1, 4))
            ],
            "totalAmount": round(random.uniform(20.0, 2000.0), 2),
            "currency": "USD",
            "status": random.choice(statuses),
            "shippingAddress": {
                "street": fake.street_address(),
                "city": fake.city(),
                "state": fake.state(),
                "zipCode": fake.zipcode(),
                "country": fake.country()
            },
            "paymentMethod": random.choice(["credit_card", "paypal", "bank_transfer"]),
            "orderDate": fake.date_time_between(start_date='-6m', end_date='now'),
            "shippingDate": fake.date_time_between(start_date='-5m', end_date='now') if random.random() > 0.3 else None,
            "deliveryDate": fake.date_time_between(start_date='-4m', end_date='now') if random.random() > 0.5 else None
        }
        orders.append(order)
    return orders

def main():
    """Main function to generate and insert data"""
    try:
        # Connect to MongoDB
        print("Connecting to MongoDB...")
        client = MongoClient(MONGO_URI)
        db = client[DATABASE_NAME]
        
        print(f"Connected to database: {DATABASE_NAME}")
        
        # Generate and insert users
        print("Generating users...")
        users = generate_users(50)
        result = db.users.insert_many(users)
        print(f"Inserted {len(result.inserted_ids)} users")
        
        # Generate and insert products
        print("Generating products...")
        products = generate_products(100)
        result = db.products.insert_many(products)
        print(f"Inserted {len(result.inserted_ids)} products")
        
        # Generate and insert orders
        print("Generating orders...")
        orders = generate_orders(200)
        result = db.orders.insert_many(orders)
        print(f"Inserted {len(result.inserted_ids)} orders")
        
        # Create indexes for better performance
        print("Creating indexes...")
        db.users.create_index("email", unique=True)
        db.users.create_index("username")
        db.products.create_index("category")
        db.products.create_index("productId")
        db.orders.create_index("orderId")
        db.orders.create_index("userId")
        
        print("Indexes created successfully!")
        
        # Display statistics
        print("\n=== Database Statistics ===")
        print(f"Users: {db.users.count_documents({})}")
        print(f"Products: {db.products.count_documents({})}")
        print(f"Orders: {db.orders.count_documents({})}")
        
        # Sample queries
        print("\n=== Sample Data ===")
        sample_user = db.users.find_one()
        print(f"Sample user: {sample_user['username']} ({sample_user['email']})")
        
        sample_product = db.products.find_one()
        print(f"Sample product: {sample_product['name']} - ${sample_product['price']}")
        
        print("\nData generation completed successfully!")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if 'client' in locals():
            client.close()

if __name__ == "__main__":
    main()
