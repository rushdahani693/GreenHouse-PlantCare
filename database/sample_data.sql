-- Sample data for Greenhouse/Plant Care Database

USE greenhouse_db;

-- Insert sample plants
INSERT INTO Plant (name, species, growth_stage, optimal_temp, optimal_humidity, optimal_ph) VALUES
('Tomato Plant', 'Solanum lycopersicum', 'Fruiting', 24.5, 65.0, 6.2),
('Basil', 'Ocimum basilicum', 'Vegetative', 22.0, 55.0, 6.5),
('Rose Bush', 'Rosa damascena', 'Blooming', 18.0, 60.0, 6.8),
('Cactus', 'Echinocactus grusonii', 'Mature', 30.0, 20.0, 6.0),
('Orchid', 'Phalaenopsis amabilis', 'Flowering', 21.0, 70.0, 5.8);

-- Insert sample sensor data
INSERT INTO SensorData (plant_id, temperature, humidity, soil_moisture, ph_level, light_intensity) VALUES
(1, 25.2, 63.5, 45.2, 6.1, 800.5),
(1, 24.8, 66.2, 47.8, 6.3, 750.2),
(2, 23.1, 54.8, 42.1, 6.6, 600.0),
(2, 21.9, 56.3, 39.7, 6.4, 580.3),
(3, 19.5, 58.7, 51.2, 6.7, 720.1),
(3, 17.8, 61.3, 53.8, 6.9, 680.4),
(4, 32.1, 18.5, 15.3, 5.9, 950.7),
(4, 29.8, 21.2, 17.8, 6.1, 920.3),
(5, 22.3, 69.8, 58.4, 5.7, 450.2),
(5, 20.7, 72.1, 61.7, 5.9, 420.8);

-- Insert sample care schedules
INSERT INTO CareSchedule (plant_id, irrigation_time, water_amount, nutrient_amount, frequency) VALUES
(1, '08:00:00', 500.0, 10.0, 'Daily'),
(1, '18:00:00', 300.0, 5.0, 'Daily'),
(2, '09:00:00', 200.0, 15.0, 'Every other day'),
(3, '07:30:00', 800.0, 20.0, 'Weekly'),
(4, '10:00:00', 100.0, 2.0, 'Weekly'),
(5, '11:00:00', 150.0, 8.0, 'Twice weekly');

-- Insert sample alerts
INSERT INTO Alerts (plant_id, message, severity) VALUES
(1, 'Temperature above optimal range', 'medium'),
(2, 'Humidity below optimal range', 'low'),
(4, 'Soil moisture critically low', 'high'),
(5, 'pH level dropping rapidly', 'medium');