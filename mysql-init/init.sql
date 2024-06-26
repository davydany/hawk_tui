CREATE TABLE employees (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    department VARCHAR(100)
);

INSERT INTO employees (name, email, department) VALUES
('John Doe', 'john.doe@example.com', 'IT'),
('Jane Smith', 'jane.smith@example.com', 'HR'),
('Mike Johnson', 'mike.johnson@example.com', 'Marketing');