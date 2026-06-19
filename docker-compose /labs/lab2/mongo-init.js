// MongoDB initialization script
// This script runs when the container starts for the first time

// Switch to the test database
db = db.getSiblingDB('testdb');

// Create a collection for sample data
db.createCollection('users');

// Create a collection for products
db.createCollection('products');

// Create indexes for better performance
db.users.createIndex({ "email": 1 }, { unique: true });
db.products.createIndex({ "category": 1 });

print('MongoDB initialization completed successfully!');
