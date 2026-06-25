import sqlite3
from config import Config

def setup_database():
    """Initialize database and add sample data"""
    conn = sqlite3.connect(Config.DATABASE)
    cursor = conn.cursor()
    
    # Create tables
    print("Creating tables...")
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Plant (
            plant_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            species TEXT,
            growth_stage TEXT,
            optimal_temp REAL,
            optimal_humidity REAL,
            optimal_ph REAL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS SensorData (
            data_id INTEGER PRIMARY KEY AUTOINCREMENT,
            plant_id INTEGER,
            temperature REAL,
            humidity REAL,
            soil_moisture REAL,
            ph_level REAL,
            light_intensity REAL,
            recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (plant_id) REFERENCES Plant(plant_id) ON DELETE CASCADE
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS CareSchedule (
            schedule_id INTEGER PRIMARY KEY AUTOINCREMENT,
            plant_id INTEGER,
            irrigation_time TEXT,
            water_amount REAL,
            nutrient_amount REAL,
            frequency TEXT,
            FOREIGN KEY (plant_id) REFERENCES Plant(plant_id) ON DELETE CASCADE
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Alerts (
            alert_id INTEGER PRIMARY KEY AUTOINCREMENT,
            plant_id INTEGER,
            message TEXT,
            severity TEXT CHECK(severity IN ('low', 'medium', 'high', 'critical')),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (plant_id) REFERENCES Plant(plant_id) ON DELETE CASCADE
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Caretaker (
            caretaker_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT,
            phone TEXT,
            specialization TEXT,
            hire_date DATE
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Location (
            location_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            type TEXT,
            size REAL,
            temperature_control TEXT,
            humidity_control TEXT,
            capacity INTEGER
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Fertilizer (
            fertilizer_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            type TEXT,
            npk_ratio TEXT,
            quantity_available REAL,
            unit TEXT,
            cost_per_unit REAL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS PlantCare (
            care_id INTEGER PRIMARY KEY AUTOINCREMENT,
            plant_id INTEGER,
            caretaker_id INTEGER,
            care_date DATE,
            care_type TEXT,
            notes TEXT,
            FOREIGN KEY (plant_id) REFERENCES Plant(plant_id) ON DELETE CASCADE,
            FOREIGN KEY (caretaker_id) REFERENCES Caretaker(caretaker_id) ON DELETE SET NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS FertilizerApplication (
            application_id INTEGER PRIMARY KEY AUTOINCREMENT,
            plant_id INTEGER,
            fertilizer_id INTEGER,
            caretaker_id INTEGER,
            amount REAL,
            application_date DATE,
            notes TEXT,
            FOREIGN KEY (plant_id) REFERENCES Plant(plant_id) ON DELETE CASCADE,
            FOREIGN KEY (fertilizer_id) REFERENCES Fertilizer(fertilizer_id) ON DELETE CASCADE,
            FOREIGN KEY (caretaker_id) REFERENCES Caretaker(caretaker_id) ON DELETE SET NULL
        )
    ''')
    
    conn.commit()
    print("Tables created successfully!")
    
    # Check if data already exists
    cursor.execute("SELECT COUNT(*) FROM Plant")
    count = cursor.fetchone()[0]
    
    if count > 0:
        print(f"Database already contains {count} plants. Skipping sample data insertion.")
    else:
        print("Inserting sample data...")
        
        # Insert sample plants
        plants = [
            ('Tomato Plant', 'Solanum lycopersicum', 'Fruiting', 24.5, 65.0, 6.2),
            ('Basil', 'Ocimum basilicum', 'Vegetative', 22.0, 55.0, 6.5),
            ('Rose Bush', 'Rosa damascena', 'Blooming', 18.0, 60.0, 6.8),
            ('Cactus', 'Echinocactus grusonii', 'Mature', 30.0, 20.0, 6.0),
            ('Orchid', 'Phalaenopsis amabilis', 'Flowering', 21.0, 70.0, 5.8)
        ]
        
        cursor.executemany('''
            INSERT INTO Plant (name, species, growth_stage, optimal_temp, optimal_humidity, optimal_ph)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', plants)
        
        # Insert sample sensor data
        sensor_data = [
            (1, 25.2, 63.5, 45.2, 6.1, 800.5),
            (1, 24.8, 66.2, 47.8, 6.3, 750.2),
            (2, 23.1, 54.8, 42.1, 6.6, 600.0),
            (2, 21.9, 56.3, 39.7, 6.4, 580.3),
            (3, 19.5, 58.7, 51.2, 6.7, 720.1),
            (3, 17.8, 61.3, 53.8, 6.9, 680.4),
            (4, 32.1, 18.5, 15.3, 5.9, 950.7),
            (4, 29.8, 21.2, 17.8, 6.1, 920.3),
            (5, 22.3, 69.8, 58.4, 5.7, 450.2),
            (5, 20.7, 72.1, 61.7, 5.9, 420.8)
        ]
        
        cursor.executemany('''
            INSERT INTO SensorData (plant_id, temperature, humidity, soil_moisture, ph_level, light_intensity)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', sensor_data)
        
        # Insert sample care schedules
        schedules = [
            (1, '08:00:00', 500.0, 10.0, 'Daily'),
            (1, '18:00:00', 300.0, 5.0, 'Daily'),
            (2, '09:00:00', 200.0, 15.0, 'Every other day'),
            (3, '07:30:00', 800.0, 20.0, 'Weekly'),
            (4, '10:00:00', 100.0, 2.0, 'Weekly'),
            (5, '11:00:00', 150.0, 8.0, 'Twice weekly')
        ]
        
        cursor.executemany('''
            INSERT INTO CareSchedule (plant_id, irrigation_time, water_amount, nutrient_amount, frequency)
            VALUES (?, ?, ?, ?, ?)
        ''', schedules)
        
        # Insert sample alerts
        alerts = [
            (1, 'Temperature above optimal range', 'medium'),
            (2, 'Humidity below optimal range', 'low'),
            (4, 'Soil moisture critically low', 'high'),
            (5, 'pH level dropping rapidly', 'medium')
        ]
        
        cursor.executemany('''
            INSERT INTO Alerts (plant_id, message, severity)
            VALUES (?, ?, ?)
        ''', alerts)
        
        # Insert sample caretakers
        caretakers = [
            ('John Smith', 'john.smith@greenhouse.com', '555-0101', 'Tropical Plants', '2023-01-15'),
            ('Sarah Johnson', 'sarah.j@greenhouse.com', '555-0102', 'Succulents', '2023-03-20'),
            ('Mike Chen', 'mike.chen@greenhouse.com', '555-0103', 'Flowering Plants', '2023-05-10')
        ]
        
        cursor.executemany('''
            INSERT INTO Caretaker (name, email, phone, specialization, hire_date)
            VALUES (?, ?, ?, ?, ?)
        ''', caretakers)
        
        # Insert sample locations
        locations = [
            ('Greenhouse A', 'Tropical', 500.0, 'Automated', 'Automated', 100),
            ('Greenhouse B', 'Temperate', 350.0, 'Manual', 'Automated', 75),
            ('Greenhouse C', 'Desert', 250.0, 'Automated', 'Manual', 50),
            ('Outdoor Garden', 'Outdoor', 1000.0, 'Natural', 'Natural', 200),
            ('Nursery Section', 'Indoor', 150.0, 'Automated', 'Automated', 40)
        ]
        
        cursor.executemany('''
            INSERT INTO Location (name, type, size, temperature_control, humidity_control, capacity)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', locations)
        
        # Insert sample fertilizers
        fertilizers = [
            ('Miracle-Gro All Purpose', 'All Purpose', '24-8-16', 50.0, 'kg', 15.99),
            ('Organic Compost', 'Organic', '5-5-5', 100.0, 'kg', 8.99),
            ('Bloom Booster', 'Flowering', '15-30-15', 25.0, 'kg', 22.99),
            ('Cactus Food', 'Specialty', '2-7-7', 10.0, 'kg', 12.99),
            ('Orchid Fertilizer', 'Specialty', '20-20-20', 15.0, 'kg', 18.99)
        ]
        
        cursor.executemany('''
            INSERT INTO Fertilizer (name, type, npk_ratio, quantity_available, unit, cost_per_unit)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', fertilizers)
        
        # Insert sample fertilizer applications
        applications = [
            (1, 1, 1, 0.5, '2024-01-15', 'Regular feeding schedule'),
            (2, 2, 1, 0.3, '2024-01-16', 'Organic application'),
            (3, 3, 2, 0.4, '2024-01-17', 'Bloom enhancement'),
            (4, 4, 2, 0.2, '2024-01-18', 'Monthly feeding'),
            (5, 5, 3, 0.25, '2024-01-19', 'Weekly application')
        ]
        
        cursor.executemany('''
            INSERT INTO FertilizerApplication (plant_id, fertilizer_id, caretaker_id, amount, application_date, notes)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', applications)
        
        conn.commit()
        print("Sample data inserted successfully!")
    
    cursor.close()
    conn.close()
    print("\nDatabase setup complete!")
    print(f"Database location: {Config.DATABASE}")

if __name__ == '__main__':
    setup_database()