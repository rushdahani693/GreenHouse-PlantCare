-- Greenhouse/Plant Care Database Schema

-- Create database
CREATE DATABASE IF NOT EXISTS greenhouse_db;
USE greenhouse_db;

-- Plant table
CREATE TABLE Plant (
    plant_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    species VARCHAR(100),
    growth_stage VARCHAR(50),
    optimal_temp DECIMAL(5,2),
    optimal_humidity DECIMAL(5,2),
    optimal_ph DECIMAL(4,2)
);

-- SensorData table
CREATE TABLE SensorData (
    data_id INT AUTO_INCREMENT PRIMARY KEY,
    plant_id INT,
    temperature DECIMAL(5,2),
    humidity DECIMAL(5,2),
    soil_moisture DECIMAL(5,2),
    ph_level DECIMAL(4,2),
    light_intensity DECIMAL(6,2),
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (plant_id) REFERENCES Plant(plant_id) ON DELETE CASCADE
);

-- CareSchedule table
CREATE TABLE CareSchedule (
    schedule_id INT AUTO_INCREMENT PRIMARY KEY,
    plant_id INT,
    irrigation_time TIME,
    water_amount DECIMAL(6,2),
    nutrient_amount DECIMAL(6,2),
    frequency VARCHAR(50),
    FOREIGN KEY (plant_id) REFERENCES Plant(plant_id) ON DELETE CASCADE
);

-- Alerts table
CREATE TABLE Alerts (
    alert_id INT AUTO_INCREMENT PRIMARY KEY,
    plant_id INT,
    message TEXT,
    severity ENUM('low', 'medium', 'high', 'critical'),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (plant_id) REFERENCES Plant(plant_id) ON DELETE CASCADE
);