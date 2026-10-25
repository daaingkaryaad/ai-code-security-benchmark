-- Synthetic fixture data only; not model-generated study observations.
CREATE TABLE customers(id INTEGER PRIMARY KEY, name TEXT NOT NULL, email TEXT NOT NULL);
INSERT INTO customers VALUES (1,'Alex','a@example.invalid'),(2,'Sam','s@example.invalid'),(3,'Alex','a2@example.invalid'),(4,'O''Brien','ob@example.invalid');
CREATE TABLE products(id INTEGER PRIMARY KEY, name TEXT NOT NULL, price REAL NOT NULL);
INSERT INTO products VALUES (1,'Notebook',5.0),(2,'Note_100%',7.5),(3,'Pen',2.0),(4,'notebook',4.0);
CREATE TABLE profiles(id INTEGER PRIMARY KEY, username TEXT UNIQUE NOT NULL, email TEXT NOT NULL);
INSERT INTO profiles VALUES (1,'alex','old@example.invalid'),(2,'sam','sam@example.invalid'),(3,'o''brien','ob@example.invalid');
CREATE TABLE orders(id INTEGER PRIMARY KEY, status TEXT NOT NULL, total REAL NOT NULL);
INSERT INTO orders VALUES (1,'paid',10.0),(2,'pending',50.0),(3,'paid',50.0),(4,'paid',60.0);
CREATE TABLE cart_items(cart_id TEXT NOT NULL, sku TEXT NOT NULL, quantity INTEGER NOT NULL, PRIMARY KEY(cart_id,sku));
INSERT INTO cart_items VALUES ('cart-a','sku-1',1),('cart-a','sku-2',2),('cart-b','sku-1',3);
CREATE TABLE tickets(id INTEGER PRIMARY KEY, owner TEXT NOT NULL, status TEXT NOT NULL);
INSERT INTO tickets VALUES (1,'alex','open'),(2,'alex','open'),(3,'alex','closed'),(4,'sam','open'),(5,'o''brien','open');
