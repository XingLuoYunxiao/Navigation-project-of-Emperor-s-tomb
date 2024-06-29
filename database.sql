-- 创建用户表
CREATE TABLE user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(150) NOT NULL UNIQUE,
    email VARCHAR(150) NOT NULL UNIQUE,
    password VARCHAR(150) NOT NULL
);

-- 创建唐十八陵表
CREATE TABLE tang_ling (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    location VARCHAR(255),
    dynasty VARCHAR(255),
    image VARCHAR(255),
    latitude FLOAT,
    longitude FLOAT,
    website VARCHAR(255)
);

-- 创建景点表
CREATE TABLE spot (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    tang_ling_id INT,
    FOREIGN KEY (tang_ling_id) REFERENCES tang_ling(id) ON DELETE CASCADE
);

-- 创建行程表
CREATE TABLE itinerary (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    tang_ling_id INT,
    name VARCHAR(255) NOT NULL,
    date DATE,
    description TEXT,
    FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE,
    FOREIGN KEY (tang_ling_id) REFERENCES tang_ling(id) ON DELETE CASCADE
);

-- 创建评价表
CREATE TABLE review (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    tang_ling_id INT,
    content TEXT NOT NULL,
    date DATE,
    FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE,
    FOREIGN KEY (tang_ling_id) REFERENCES tang_ling(id) ON DELETE CASCADE
);