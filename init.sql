CREATE TABLE IF NOT EXISTS users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(50) NOT NULL UNIQUE,
  email VARCHAR(100),
  age INT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO users (username, email, age)
VALUES
  ('alice', 'alice@example.com', 25),
  ('bob', 'bob@example.com', 30),
  ('carol', 'carol@example.com', 22);
