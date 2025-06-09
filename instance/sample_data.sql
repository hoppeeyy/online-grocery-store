-- Insert Users
INSERT INTO Users (username, password, email, role) VALUES
('admin', 'admin123', 'admin@example.com', 'admin'),
('customer1', 'cust123', 'customer1@example.com', 'customer'),
('delivery1', 'delivery123', 'delivery1@example.com', 'delivery_agent');

-- Insert Categories
INSERT INTO Categories (name, description) VALUES
('Fruits', 'Fresh fruits'),
('Dairy', 'Milk, cheese, and eggs'),
('Bakery', 'Bread and pastries');

-- Insert Products
INSERT INTO Products (name, price, description, category_id, discount) VALUES
('Apple', 50.00, 'Fresh Kashmiri apples', 1, 5.00),
('Milk', 60.00, '1L toned milk', 2, 0.00),
('Bread', 40.00, 'Whole wheat bread', 3, 10.00);

-- Insert Inventory
INSERT INTO Inventory (product_id, stock, last_restocked) VALUES
(1, 100, '2023-10-01'),
(2, 50, '2023-10-05'),
(3, 30, '2023-10-10');

-- Insert Delivery Agents
INSERT INTO Delivery_Agents (user_id, vehicle_number) VALUES
(3, 'DL12AB1234');