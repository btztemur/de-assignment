CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    customer_name VARCHAR(100) NOT NULL,
    email_address VARCHAR(100) UNIQUE NOT NULL,
    country VARCHAR(50) NOT NULL,
    phone_number VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    price NUMERIC(10, 2) NOT NULL,
    category VARCHAR(50) NOT NULL,
    stock_quantity INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE sales_transactions (
    transaction_id SERIAL PRIMARY KEY,
    customer_id INT NOT NULL,
    product_id INT NOT NULL,
    purchase_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    quantity_purchased INT NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE CASCADE
);

CREATE TABLE shipping_details (
    transaction_id INT PRIMARY KEY,
    shipping_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    shipping_address VARCHAR(255) NOT NULL,
    city VARCHAR(100) NOT NULL,
    country VARCHAR(50) NOT NULL,
    postal_code VARCHAR(20),
    FOREIGN KEY (transaction_id) REFERENCES sales_transactions(transaction_id) ON DELETE CASCADE
);

/* 
 this query joins two tables: sales_transactions with products, multiplies two columns: quantity_pruchased with price, calculates 
 sum os this product by grouping month and year and selects year,month and total sum.
 */
SELECT
    EXTRACT(YEAR FROM s.purchase_date) AS year,
    EXTRACT(MONTH FROM s.purchase_date) AS month,
    sum(s.quantity_purchased * p.price)
FROM
    sales_transactions s
JOIN products p ON s.product_id = p.product_id 
GROUP BY
    EXTRACT(YEAR FROM purchase_date),
    EXTRACT(MONTH FROM purchase_date);
/*
 this query joins two tables: sales_transactions with  products,  multiplies two columns: quantity_pruchased with price,
 sum os this product by grouping month and year, orders by year and month, and calculates average over preceding two months and current month
*/
SELECT
        EXTRACT(YEAR FROM s.purchase_date) AS year,
        EXTRACT(MONTH FROM s.purchase_date) AS month,
        AVG(sum(s.quantity_purchased * p.price)) OVER (
            ORDER by EXTRACT(YEAR FROM s.purchase_date), EXTRACT(MONTH FROM s.purchase_date)
            ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
        ) AS three_month_moving_avg
    FROM
        sales_transactions s
    join products p on s.product_id = p.product_id 
    GROUP BY
        EXTRACT(YEAR FROM purchase_date),
        EXTRACT(MONTH FROM purchase_date);