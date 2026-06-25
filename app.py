from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from config import Config
import datetime

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = app.config['SECRET_KEY']

# Database connection
def get_db_connection():
    connection = sqlite3.connect(app.config['DATABASE'])
    connection.row_factory = sqlite3.Row  # This enables column access by name
    return connection

# Initialize database
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create tables
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
    conn.close()

# Helper functions
def check_alerts(plant_id, temperature, humidity, soil_moisture, ph_level):
    """Check if sensor values are outside optimal range and create alerts"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get plant optimal values
    cursor.execute("SELECT * FROM Plant WHERE plant_id = ?", (plant_id,))
    plant = cursor.fetchone()
    
    if plant:
        alerts = []
        
        # Check temperature
        if temperature > plant['optimal_temp'] * 1.1:  # 10% above optimal
            alerts.append(f"High temperature: {temperature}°C (optimal: {plant['optimal_temp']}°C)")
        elif temperature < plant['optimal_temp'] * 0.9:  # 10% below optimal
            alerts.append(f"Low temperature: {temperature}°C (optimal: {plant['optimal_temp']}°C)")
            
        # Check humidity
        if humidity > plant['optimal_humidity'] * 1.1:
            alerts.append(f"High humidity: {humidity}% (optimal: {plant['optimal_humidity']}%)")
        elif humidity < plant['optimal_humidity'] * 0.9:
            alerts.append(f"Low humidity: {humidity}% (optimal: {plant['optimal_humidity']}%)")
            
        # Check pH
        if ph_level > plant['optimal_ph'] * 1.05:  # 5% above optimal
            alerts.append(f"High pH level: {ph_level} (optimal: {plant['optimal_ph']})")
        elif ph_level < plant['optimal_ph'] * 0.95:  # 5% below optimal
            alerts.append(f"Low pH level: {ph_level} (optimal: {plant['optimal_ph']})")
            
        # Create alerts in database
        for alert_msg in alerts:
            severity = 'medium'
            if 'High' in alert_msg or 'Low' in alert_msg:
                severity = 'high' if 'High' in alert_msg or 'Low' in alert_msg else 'low'
                
            cursor.execute(
                "INSERT INTO Alerts (plant_id, message, severity) VALUES (?, ?, ?)",
                (plant_id, alert_msg, severity)
            )
        
        conn.commit()
    
    cursor.close()
    conn.close()

# Routes
@app.route('/')
def dashboard():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get plants count
    cursor.execute("SELECT COUNT(*) as count FROM Plant")
    plants_count = cursor.fetchone()['count']
    
    # Get recent alerts
    cursor.execute("""
        SELECT a.*, p.name as plant_name 
        FROM Alerts a 
        JOIN Plant p ON a.plant_id = p.plant_id 
        ORDER BY a.created_at DESC 
        LIMIT 5
    """)
    recent_alerts = cursor.fetchall()
    
    # Get recent sensor data
    cursor.execute("""
        SELECT s.*, p.name as plant_name 
        FROM SensorData s 
        JOIN Plant p ON s.plant_id = p.plant_id 
        ORDER BY s.recorded_at DESC 
        LIMIT 5
    """)
    recent_sensors = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template('index.html', 
                          plants_count=plants_count,
                          recent_alerts=recent_alerts,
                          recent_sensors=recent_sensors)

@app.route('/plants')
def plants():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM Plant")
    plants = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template('plants.html', plants=plants)

@app.route('/plants/add', methods=['GET', 'POST'])
def add_plant():
    if request.method == 'POST':
        name = request.form['name']
        species = request.form['species']
        growth_stage = request.form['growth_stage']
        optimal_temp = request.form['optimal_temp']
        optimal_humidity = request.form['optimal_humidity']
        optimal_ph = request.form['optimal_ph']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO Plant (name, species, growth_stage, optimal_temp, optimal_humidity, optimal_ph)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (name, species, growth_stage, optimal_temp, optimal_humidity, optimal_ph))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        flash('Plant added successfully!', 'success')
        return redirect(url_for('plants'))
    
    return render_template('add_plant.html')

@app.route('/plants/edit/<int:plant_id>', methods=['GET', 'POST'])
def edit_plant(plant_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if request.method == 'POST':
        name = request.form['name']
        species = request.form['species']
        growth_stage = request.form['growth_stage']
        optimal_temp = request.form['optimal_temp']
        optimal_humidity = request.form['optimal_humidity']
        optimal_ph = request.form['optimal_ph']
        
        cursor.execute("""
            UPDATE Plant 
            SET name=?, species=?, growth_stage=?, optimal_temp=?, optimal_humidity=?, optimal_ph=?
            WHERE plant_id=?
        """, (name, species, growth_stage, optimal_temp, optimal_humidity, optimal_ph, plant_id))
        
        conn.commit()
        flash('Plant updated successfully!', 'success')
        return redirect(url_for('plants'))
    
    cursor.execute("SELECT * FROM Plant WHERE plant_id = ?", (plant_id,))
    plant = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    if plant:
        return render_template('edit_plant.html', plant=plant)
    else:
        flash('Plant not found!', 'error')
        return redirect(url_for('plants'))

@app.route('/plants/delete/<int:plant_id>')
def delete_plant(plant_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM Plant WHERE plant_id = ?", (plant_id,))
    conn.commit()
    
    cursor.close()
    conn.close()
    
    flash('Plant deleted successfully!', 'success')
    return redirect(url_for('plants'))

@app.route('/sensor/<int:plant_id>')
def sensor_data(plant_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get plant info
    cursor.execute("SELECT * FROM Plant WHERE plant_id = ?", (plant_id,))
    plant = cursor.fetchone()
    
    if not plant:
        flash('Plant not found!', 'error')
        return redirect(url_for('plants'))
    
    # Get sensor data
    cursor.execute("""
        SELECT * FROM SensorData 
        WHERE plant_id = ? 
        ORDER BY recorded_at DESC
    """, (plant_id,))
    sensor_data = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template('sensor.html', plant=plant, sensor_data=sensor_data)

@app.route('/sensor/add/<int:plant_id>', methods=['POST'])
def add_sensor_data(plant_id):
    temperature = float(request.form['temperature'])
    humidity = float(request.form['humidity'])
    soil_moisture = float(request.form['soil_moisture'])
    ph_level = float(request.form['ph_level'])
    light_intensity = float(request.form['light_intensity'])
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO SensorData (plant_id, temperature, humidity, soil_moisture, ph_level, light_intensity)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (plant_id, temperature, humidity, soil_moisture, ph_level, light_intensity))
    
    conn.commit()
    cursor.close()
    conn.close()
    
    # Check for alerts
    check_alerts(plant_id, temperature, humidity, soil_moisture, ph_level)
    
    flash('Sensor data added successfully!', 'success')
    return redirect(url_for('sensor_data', plant_id=plant_id))

@app.route('/schedule/<int:plant_id>')
def care_schedule(plant_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get plant info
    cursor.execute("SELECT * FROM Plant WHERE plant_id = ?", (plant_id,))
    plant = cursor.fetchone()
    
    if not plant:
        flash('Plant not found!', 'error')
        return redirect(url_for('plants'))
    
    # Get care schedule
    cursor.execute("""
        SELECT * FROM CareSchedule 
        WHERE plant_id = ? 
        ORDER BY schedule_id DESC
    """, (plant_id,))
    schedules = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template('schedule.html', plant=plant, schedules=schedules)

@app.route('/schedule/add/<int:plant_id>', methods=['POST'])
def add_care_schedule(plant_id):
    irrigation_time = request.form['irrigation_time']
    water_amount = request.form['water_amount']
    nutrient_amount = request.form['nutrient_amount']
    frequency = request.form['frequency']
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO CareSchedule (plant_id, irrigation_time, water_amount, nutrient_amount, frequency)
        VALUES (?, ?, ?, ?, ?)
    """, (plant_id, irrigation_time, water_amount, nutrient_amount, frequency))
    
    conn.commit()
    cursor.close()
    conn.close()
    
    flash('Care schedule added successfully!', 'success')
    return redirect(url_for('care_schedule', plant_id=plant_id))

@app.route('/alerts/<int:plant_id>')
def alerts(plant_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get plant info
    cursor.execute("SELECT * FROM Plant WHERE plant_id = ?", (plant_id,))
    plant = cursor.fetchone()
    
    if not plant:
        flash('Plant not found!', 'error')
        return redirect(url_for('plants'))
    
    # Get alerts
    cursor.execute("""
        SELECT * FROM Alerts 
        WHERE plant_id = ? 
        ORDER BY created_at DESC
    """, (plant_id,))
    alerts = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template('alerts.html', plant=plant, alerts=alerts)

# Caretaker Routes
@app.route('/caretakers')
def caretakers():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM Caretaker ORDER BY caretaker_id")
    caretakers = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template('caretakers.html', caretakers=caretakers)

@app.route('/caretakers/add', methods=['GET', 'POST'])
def add_caretaker():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        specialization = request.form['specialization']
        hire_date = request.form['hire_date']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO Caretaker (name, email, phone, specialization, hire_date)
            VALUES (?, ?, ?, ?, ?)
        """, (name, email, phone, specialization, hire_date))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        flash('Caretaker added successfully!', 'success')
        return redirect(url_for('caretakers'))
    
    return render_template('add_caretaker.html')

@app.route('/caretakers/edit/<int:caretaker_id>', methods=['GET', 'POST'])
def edit_caretaker(caretaker_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        specialization = request.form['specialization']
        hire_date = request.form['hire_date']
        
        cursor.execute("""
            UPDATE Caretaker 
            SET name=?, email=?, phone=?, specialization=?, hire_date=?
            WHERE caretaker_id=?
        """, (name, email, phone, specialization, hire_date, caretaker_id))
        
        conn.commit()
        flash('Caretaker updated successfully!', 'success')
        return redirect(url_for('caretakers'))
    
    cursor.execute("SELECT * FROM Caretaker WHERE caretaker_id = ?", (caretaker_id,))
    caretaker = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    if caretaker:
        return render_template('edit_caretaker.html', caretaker=caretaker)
    else:
        flash('Caretaker not found!', 'error')
        return redirect(url_for('caretakers'))

@app.route('/caretakers/delete/<int:caretaker_id>')
def delete_caretaker(caretaker_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM Caretaker WHERE caretaker_id = ?", (caretaker_id,))
    conn.commit()
    
    cursor.close()
    conn.close()
    
    flash('Caretaker deleted successfully!', 'success')
    return redirect(url_for('caretakers'))

# Location Routes
@app.route('/locations')
def locations():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM Location ORDER BY location_id")
    locations = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template('locations.html', locations=locations)

@app.route('/locations/add', methods=['GET', 'POST'])
def add_location():
    if request.method == 'POST':
        name = request.form['name']
        type = request.form['type']
        size = request.form['size']
        temperature_control = request.form['temperature_control']
        humidity_control = request.form['humidity_control']
        capacity = request.form['capacity']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO Location (name, type, size, temperature_control, humidity_control, capacity)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (name, type, size, temperature_control, humidity_control, capacity))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        flash('Location added successfully!', 'success')
        return redirect(url_for('locations'))
    
    return render_template('add_location.html')

@app.route('/locations/edit/<int:location_id>', methods=['GET', 'POST'])
def edit_location(location_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if request.method == 'POST':
        name = request.form['name']
        type = request.form['type']
        size = request.form['size']
        temperature_control = request.form['temperature_control']
        humidity_control = request.form['humidity_control']
        capacity = request.form['capacity']
        
        cursor.execute("""
            UPDATE Location 
            SET name=?, type=?, size=?, temperature_control=?, humidity_control=?, capacity=?
            WHERE location_id=?
        """, (name, type, size, temperature_control, humidity_control, capacity, location_id))
        
        conn.commit()
        flash('Location updated successfully!', 'success')
        return redirect(url_for('locations'))
    
    cursor.execute("SELECT * FROM Location WHERE location_id = ?", (location_id,))
    location = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    if location:
        return render_template('edit_location.html', location=location)
    else:
        flash('Location not found!', 'error')
        return redirect(url_for('locations'))

@app.route('/locations/delete/<int:location_id>')
def delete_location(location_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM Location WHERE location_id = ?", (location_id,))
    conn.commit()
    
    cursor.close()
    conn.close()
    
    flash('Location deleted successfully!', 'success')
    return redirect(url_for('locations'))

# Fertilizer Routes
@app.route('/fertilizers')
def fertilizers():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM Fertilizer ORDER BY fertilizer_id")
    fertilizers = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template('fertilizers.html', fertilizers=fertilizers)

@app.route('/fertilizers/add', methods=['GET', 'POST'])
def add_fertilizer():
    if request.method == 'POST':
        name = request.form['name']
        type = request.form['type']
        npk_ratio = request.form['npk_ratio']
        quantity_available = request.form['quantity_available']
        unit = request.form['unit']
        cost_per_unit = request.form['cost_per_unit']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO Fertilizer (name, type, npk_ratio, quantity_available, unit, cost_per_unit)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (name, type, npk_ratio, quantity_available, unit, cost_per_unit))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        flash('Fertilizer added successfully!', 'success')
        return redirect(url_for('fertilizers'))
    
    return render_template('add_fertilizer.html')

@app.route('/fertilizers/edit/<int:fertilizer_id>', methods=['GET', 'POST'])
def edit_fertilizer(fertilizer_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if request.method == 'POST':
        name = request.form['name']
        type = request.form['type']
        npk_ratio = request.form['npk_ratio']
        quantity_available = request.form['quantity_available']
        unit = request.form['unit']
        cost_per_unit = request.form['cost_per_unit']
        
        cursor.execute("""
            UPDATE Fertilizer 
            SET name=?, type=?, npk_ratio=?, quantity_available=?, unit=?, cost_per_unit=?
            WHERE fertilizer_id=?
        """, (name, type, npk_ratio, quantity_available, unit, cost_per_unit, fertilizer_id))
        
        conn.commit()
        flash('Fertilizer updated successfully!', 'success')
        return redirect(url_for('fertilizers'))
    
    cursor.execute("SELECT * FROM Fertilizer WHERE fertilizer_id = ?", (fertilizer_id,))
    fertilizer = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    if fertilizer:
        return render_template('edit_fertilizer.html', fertilizer=fertilizer)
    else:
        flash('Fertilizer not found!', 'error')
        return redirect(url_for('fertilizers'))

@app.route('/fertilizers/delete/<int:fertilizer_id>')
def delete_fertilizer(fertilizer_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM Fertilizer WHERE fertilizer_id = ?", (fertilizer_id,))
    conn.commit()
    
    cursor.close()
    conn.close()
    
    flash('Fertilizer deleted successfully!', 'success')
    return redirect(url_for('fertilizers'))

# Fertilizer Application Routes
@app.route('/fertilizer-applications/<int:plant_id>')
def fertilizer_applications(plant_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get plant info
    cursor.execute("SELECT * FROM Plant WHERE plant_id = ?", (plant_id,))
    plant = cursor.fetchone()
    
    if not plant:
        flash('Plant not found!', 'error')
        return redirect(url_for('plants'))
    
    # Get fertilizer applications
    cursor.execute("""
        SELECT fa.*, f.name as fertilizer_name, c.name as caretaker_name
        FROM FertilizerApplication fa
        JOIN Fertilizer f ON fa.fertilizer_id = f.fertilizer_id
        LEFT JOIN Caretaker c ON fa.caretaker_id = c.caretaker_id
        WHERE fa.plant_id = ?
        ORDER BY fa.application_date DESC
    """, (plant_id,))
    applications = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template('fertilizer_applications.html', plant=plant, applications=applications)

@app.route('/fertilizer-applications/add/<int:plant_id>', methods=['GET', 'POST'])
def add_fertilizer_application(plant_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if request.method == 'POST':
        fertilizer_id = request.form['fertilizer_id']
        caretaker_id = request.form['caretaker_id']
        amount = request.form['amount']
        application_date = request.form['application_date']
        notes = request.form['notes']
        
        cursor.execute("""
            INSERT INTO FertilizerApplication (plant_id, fertilizer_id, caretaker_id, amount, application_date, notes)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (plant_id, fertilizer_id, caretaker_id, amount, application_date, notes))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        flash('Fertilizer application added successfully!', 'success')
        return redirect(url_for('fertilizer_applications', plant_id=plant_id))
    
    # Get fertilizers and caretakers for dropdowns
    cursor.execute("SELECT * FROM Fertilizer ORDER BY fertilizer_id")
    fertilizers = cursor.fetchall()
    
    cursor.execute("SELECT * FROM Caretaker ORDER BY caretaker_id")
    caretakers = cursor.fetchall()
    
    cursor.execute("SELECT * FROM Plant WHERE plant_id = ?", (plant_id,))
    plant = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    return render_template('add_fertilizer_application.html', plant=plant, fertilizers=fertilizers, caretakers=caretakers)

# Initialize DB when app starts (works with both gunicorn and direct run)
init_db()

if __name__ == '__main__':
    app.run(debug=True)