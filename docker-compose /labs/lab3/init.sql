-- PostgreSQL initialization script
-- This script runs when the container starts for the first time

-- Create additional schemas if needed
CREATE SCHEMA IF NOT EXISTS app_schema;

-- Set default schema
SET search_path TO app_schema, public;

-- Create users table
CREATE TABLE IF NOT EXISTS app_schema.users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    age INTEGER,
    city VARCHAR(100),
    country VARCHAR(100),
    bio TEXT,
    is_active BOOLEAN DEFAULT true,
    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create products table
CREATE TABLE IF NOT EXISTS app_schema.products (
    id SERIAL PRIMARY KEY,
    product_id VARCHAR(20) UNIQUE NOT NULL,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    category VARCHAR(50),
    price DECIMAL(10, 2),
    currency VARCHAR(3) DEFAULT 'USD',
    stock INTEGER DEFAULT 0,
    sku VARCHAR(50) UNIQUE,
    brand VARCHAR(100),
    weight DECIMAL(8, 2),
    dimensions JSONB,
    images JSONB,
    tags TEXT[],
    rating DECIMAL(2, 1),
    reviews INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create orders table
CREATE TABLE IF NOT EXISTS app_schema.orders (
    id SERIAL PRIMARY KEY,
    order_id VARCHAR(20) UNIQUE NOT NULL,
    user_id INTEGER REFERENCES app_schema.users(id),
    total_amount DECIMAL(10, 2),
    currency VARCHAR(3) DEFAULT 'USD',
    status VARCHAR(20) DEFAULT 'pending',
    shipping_address JSONB,
    payment_method VARCHAR(50),
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    shipping_date TIMESTAMP,
    delivery_date TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create order_items table
CREATE TABLE IF NOT EXISTS app_schema.order_items (
    id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES app_schema.orders(id) ON DELETE CASCADE,
    product_id INTEGER REFERENCES app_schema.products(id),
    quantity INTEGER NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_users_email ON app_schema.users(email);
CREATE INDEX IF NOT EXISTS idx_users_username ON app_schema.users(username);
CREATE INDEX IF NOT EXISTS idx_products_category ON app_schema.products(category);
CREATE INDEX IF NOT EXISTS idx_products_product_id ON app_schema.products(product_id);
CREATE INDEX IF NOT EXISTS idx_orders_order_id ON app_schema.orders(order_id);
CREATE INDEX IF NOT EXISTS idx_orders_user_id ON app_schema.orders(user_id);
CREATE INDEX IF NOT EXISTS idx_order_items_order_id ON app_schema.order_items(order_id);

-- Create trigger for updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON app_schema.users FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_products_updated_at BEFORE UPDATE ON app_schema.products FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_orders_updated_at BEFORE UPDATE ON app_schema.orders FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Insert sample data
INSERT INTO app_schema.users (username, email, first_name, last_name, age, city, country, bio) VALUES
('john_doe', 'john@example.com', 'John', 'Doe', 28, 'New York', 'USA', 'Software developer passionate about technology'),
('jane_smith', 'jane@example.com', 'Jane', 'Smith', 32, 'Los Angeles', 'USA', 'Digital marketing specialist'),
('bob_wilson', 'bob@example.com', 'Bob', 'Wilson', 45, 'Chicago', 'USA', 'Business owner and entrepreneur'),
('alice_brown', 'alice@example.com', 'Alice', 'Brown', 24, 'San Francisco', 'USA', 'UX designer and creative thinker'),
('charlie_davis', 'charlie@example.com', 'Charlie', 'Davis', 38, 'Seattle', 'USA', 'Data scientist and machine learning enthusiast')
ON CONFLICT (email) DO NOTHING;

INSERT INTO app_schema.products (product_id, name, description, category, price, stock, sku, brand, rating, reviews) VALUES
('PROD-000001', 'Wireless Headphones', 'High-quality wireless headphones with noise cancellation', 'Electronics', 199.99, 50, 'SKU-WH001', 'AudioTech', 4.5, 128),
('PROD-000002', 'Smart Watch', 'Fitness tracking smartwatch with heart rate monitor', 'Electronics', 299.99, 30, 'SKU-SW002', 'SmartGear', 4.3, 89),
('PROD-000003', 'Running Shoes', 'Comfortable running shoes for daily exercise', 'Sports', 89.99, 100, 'SKU-RS003', 'SportMax', 4.7, 256),
('PROD-000004', 'Coffee Maker', 'Automatic coffee maker with programmable timer', 'Home & Garden', 149.99, 25, 'SKU-CM004', 'BrewMaster', 4.4, 67),
('PROD-000005', 'Yoga Mat', 'Non-slip exercise yoga mat for home workouts', 'Sports', 29.99, 75, 'SKU-YM005', 'FitLife', 4.6, 143)
ON CONFLICT (product_id) DO NOTHING;

PRINT 'PostgreSQL initialization completed successfully!';
