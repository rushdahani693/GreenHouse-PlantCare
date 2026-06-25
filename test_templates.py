from flask import Flask, render_template_string
from jinja2 import Environment, FileSystemLoader
import os

# Set up Jinja2 environment
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
env = Environment(loader=FileSystemLoader(template_dir))

# Test rendering each template with sample data
def test_template_rendering():
    # Sample data for testing
    sample_plant = {
        'plant_id': 1,
        'name': 'Tomato Plant',
        'species': 'Solanum lycopersicum',
        'growth_stage': 'Fruiting',
        'optimal_temp': 24.5,
        'optimal_humidity': 65.0,
        'optimal_ph': 6.2
    }
    
    sample_plants = [sample_plant]
    
    sample_sensor_data = [
        {
            'recorded_at': '2023-06-15 10:30:00',
            'temperature': 25.2,
            'humidity': 63.5,
            'soil_moisture': 45.2,
            'ph_level': 6.1,
            'light_intensity': 800.5
        }
    ]
    
    sample_schedules = [
        {
            'schedule_id': 1,
            'irrigation_time': '08:00:00',
            'water_amount': 500.0,
            'nutrient_amount': 10.0,
            'frequency': 'Daily'
        }
    ]
    
    sample_alerts = [
        {
            'created_at': '2023-06-15 09:15:00',
            'message': 'Temperature above optimal range',
            'severity': 'medium'
        }
    ]
    
    # Test each template
    templates_to_test = [
        ('index.html', {'plants_count': 5, 'recent_alerts': sample_alerts[:1], 'recent_sensors': sample_sensor_data[:1]}),
        ('plants.html', {'plants': sample_plants}),
        ('add_plant.html', {}),
        ('edit_plant.html', {'plant': sample_plant}),
        ('sensor.html', {'plant': sample_plant, 'sensor_data': sample_sensor_data}),
        ('schedule.html', {'plant': sample_plant, 'schedules': sample_schedules}),
        ('alerts.html', {'plant': sample_plant, 'alerts': sample_alerts})
    ]
    
    print("Testing template rendering...")
    
    for template_name, context in templates_to_test:
        try:
            template = env.get_template(template_name)
            rendered = template.render(**context)
            print(f"✓ {template_name} rendered successfully ({len(rendered)} characters)")
        except Exception as e:
            print(f"✗ {template_name} failed to render: {str(e)}")
    
    print("Template testing completed.")

if __name__ == '__main__':
    test_template_rendering()