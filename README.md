# Greenhouse Plant Care Database Application

A Flask-based web application for monitoring and managing greenhouse plants with MySQL database backend.

## Features

- Plant inventory management (CRUD operations)
- Sensor data monitoring (temperature, humidity, soil moisture, pH, light intensity)
- Care scheduling (irrigation and nutrient management)
- Automated alerts when conditions exceed optimal ranges
- Dashboard with overview of all plants and recent alerts

## Prerequisites

- Python 3.7 or higher
- MySQL Server
- pip (Python package installer)

## Installation

1. Clone or download this repository
2. Navigate to the project directory:
   ```
   cd greenhouse_app
   ```

3. Install required Python packages:
   ```
   pip install -r requirements.txt
   ```

4. Set up the MySQL database:
   - Create a MySQL database (default name: `greenhouse_db`)
   - Execute the schema file:
     ```
     mysql -u [username] -p [database_name] < database/schema.sql
     ```
   - (Optional) Load sample data:
     ```
     mysql -u [username] -p [database_name] < database/sample_data.sql
     ```

5. Configure database connection:
   - Update `config.py` with your MySQL credentials, or
   - Set environment variables:
     ```
     export MYSQL_HOST=localhost
     export MYSQL_USER=your_username
     export MYSQL_PASSWORD=your_password
     export MYSQL_DB=greenhouse_db
     export SECRET_KEY=your_secret_key
     ```

## Running the Application

1. Start the Flask development server:
   ```
   python app.py
   ```

2. Open your web browser and navigate to:
   ```
   http://localhost:5000
   ```

## Project Structure

```
greenhouse_app/
├── app.py              # Main Flask application
├── config.py           # Configuration settings
├── requirements.txt    # Python dependencies
├── README.md           # This file
├── /database/
│   ├── schema.sql      # Database schema
│   └── sample_data.sql # Sample data
├── /templates/
│   ├── base.html       # Base template
│   ├── index.html      # Dashboard
│   ├── plants.html     # Plant list
│   ├── add_plant.html  # Add plant form
│   ├── edit_plant.html # Edit plant form
│   ├── sensor.html     # Sensor data
│   ├── schedule.html   # Care schedule
│   └── alerts.html     # Alerts
└── /static/
    └── styles.css      # Custom CSS styles
```

## Usage

1. **Dashboard**: View an overview of your greenhouse including total plants, recent alerts, and sensor readings.

2. **Plants**: 
   - View all plants in your inventory
   - Add new plants with their optimal growing conditions
   - Edit or delete existing plants

3. **Sensor Data**: 
   - View historical sensor readings for each plant
   - Add new sensor readings
   - See alerts when conditions exceed optimal ranges

4. **Care Schedule**: 
   - View and add irrigation/nutrient schedules
   - Manage watering and feeding frequency

5. **Alerts**: 
   - View all alerts for a specific plant
   - See severity levels of different alerts

## Database Schema

The application uses four main tables:

1. **Plant**: Stores plant information and optimal growing conditions
2. **SensorData**: Records environmental sensor readings
3. **CareSchedule**: Manages irrigation and nutrient schedules
4. **Alerts**: Stores automated alerts when conditions exceed optimal ranges

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a pull request

## License

This project is licensed under the MIT License.