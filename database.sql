CREATE DATABASE IF NOT EXISTS village_sattam;
USE village_sattam;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    village VARCHAR(100),
    is_admin TINYINT(1) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS schemes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    eligibility TEXT,
    benefits TEXT,
    category VARCHAR(100) DEFAULT 'General',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS complaints (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    title VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    status ENUM('Pending', 'In Progress', 'Resolved', 'Rejected') DEFAULT 'Pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS announcements (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO users (name, email, password, village, is_admin) VALUES
('Admin', 'admin@villagesattam.gov.in', 'scrypt:32768:8:1$XQ1cVhv2VnL8nIgO$e4a7b6c2d1e0f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0', 'District HQ', 1);

INSERT INTO schemes (title, description, eligibility, benefits, category) VALUES
('PM Kisan Samman Nidhi', 'Direct income support scheme for small and marginal farmers providing financial assistance of Rs. 6000 per year.', 'All small and marginal farmers with cultivable land up to 2 hectares. Must be Indian citizen.', 'Rs. 6000 per year in 3 installments of Rs. 2000 each directly to bank account.', 'Agriculture'),
('Pradhan Mantri Awas Yojana', 'Housing for All mission to provide affordable housing to the urban and rural poor by 2022.', 'BPL families, SC/ST, minorities, women-headed households. Annual income below Rs. 3 lakhs.', 'Subsidy of Rs. 1.5 lakh on home loans up to Rs. 6 lakhs. Financial assistance for house construction.', 'Housing'),
('Ayushman Bharat - PMJAY', 'World''s largest government-funded health insurance/assurance scheme providing health coverage.', 'Families identified based on SECC 2011 data. Bottom 40% of Indian population.', 'Health cover of Rs. 5 lakhs per family per year for secondary and tertiary care hospitalization.', 'Health'),
('PM Ujjwala Yojana', 'Scheme to provide LPG connections to women belonging to BPL households in India.', 'Women above 18 years from BPL households. Should not already have LPG connection.', 'Free LPG connection with financial assistance of Rs. 1600. First refill and stove free.', 'Energy'),
('Kisan Credit Card', 'Credit scheme to provide adequate and timely credit to farmers for agricultural and allied activities.', 'All farmers, sharecroppers, tenant farmers and oral lessees engaged in agriculture.', 'Short-term credit requirements up to Rs. 3 lakhs at reduced interest rate of 4% per annum.', 'Agriculture'),
('PM Mudra Yojana', 'Micro Units Development & Refinance Agency scheme to fund small business enterprises.', 'Non-farm small/micro enterprises generating income from manufacturing, trading or services.', 'Loans up to Rs. 10 lakhs categorized as Shishu (upto 50k), Kishor (50k-5L), Tarun (5L-10L).', 'Business');

INSERT INTO announcements (title, content) VALUES
('Village Panchayat Meeting - March 2025', 'All villagers are invited to attend the monthly Gram Panchayat meeting on 15th March 2025 at the Community Hall at 10:00 AM.'),
('Free Health Camp', 'A free health checkup camp will be organized on 20th March 2025 at the Primary Health Centre. All residents are requested to attend.'),
('Ration Card Update', 'All families are requested to update their Ration Card details at the Panchayat office before 31st March 2025.'),

('Water Supply Schedule', 'Due to pipeline maintenance, water supply will be disrupted on 18th March 2025 from 9 AM to 5 PM. Please store water in advance.');

