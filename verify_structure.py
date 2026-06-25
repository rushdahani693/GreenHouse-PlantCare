import os

def verify_project_structure():
    """Verify that all required files and directories exist"""
    
    required_files = [
        'app.py',
        'config.py',
        'requirements.txt',
        'README.md',
        'database/schema.sql',
        'database/sample_data.sql',
        'static/styles.css',
        'templates/base.html',
        'templates/index.html',
        'templates/plants.html',
        'templates/add_plant.html',
        'templates/edit_plant.html',
        'templates/sensor.html',
        'templates/schedule.html',
        'templates/alerts.html'
    ]
    
    missing_files = []
    
    for file_path in required_files:
        full_path = os.path.join(os.getcwd(), file_path)
        if not os.path.exists(full_path):
            missing_files.append(file_path)
    
    if missing_files:
        print("❌ Missing files:")
        for file_path in missing_files:
            print(f"  - {file_path}")
        return False
    else:
        print("✅ All required files are present")
        return True

def verify_database_schema():
    """Verify that the database schema contains required tables"""
    
    schema_path = os.path.join(os.getcwd(), 'database', 'schema.sql')
    
    if not os.path.exists(schema_path):
        print("❌ Database schema file not found")
        return False
    
    with open(schema_path, 'r') as f:
        content = f.read()
    
    required_tables = ['Plant', 'SensorData', 'CareSchedule', 'Alerts']
    missing_tables = []
    
    for table in required_tables:
        if f'CREATE TABLE {table}' not in content:
            missing_tables.append(table)
    
    if missing_tables:
        print("❌ Missing tables in schema:")
        for table in missing_tables:
            print(f"  - {table}")
        return False
    else:
        print("✅ All required tables are defined in schema")
        return True

def verify_flask_routes():
    """Verify that app.py contains required routes"""
    
    app_path = os.path.join(os.getcwd(), 'app.py')
    
    if not os.path.exists(app_path):
        print("❌ app.py file not found")
        return False
    
    with open(app_path, 'r') as f:
        content = f.read()
    
    required_routes = [
        "@app.route('/')",
        "@app.route('/plants')",
        "@app.route('/plants/add')",
        "@app.route('/sensor/<int:plant_id>')",
        "@app.route('/schedule/<int:plant_id>')",
        "@app.route('/alerts/<int:plant_id>')"
    ]
    
    missing_routes = []
    
    for route in required_routes:
        if route not in content:
            missing_routes.append(route)
    
    if missing_routes:
        print("❌ Missing routes in app.py:")
        for route in missing_routes:
            print(f"  - {route}")
        return False
    else:
        print("✅ All required routes are defined in app.py")
        return True

def verify_templates():
    """Verify that templates directory contains required files"""
    
    templates_dir = os.path.join(os.getcwd(), 'templates')
    
    if not os.path.exists(templates_dir):
        print("❌ Templates directory not found")
        return False
    
    required_templates = [
        'base.html',
        'index.html',
        'plants.html',
        'add_plant.html',
        'edit_plant.html',
        'sensor.html',
        'schedule.html',
        'alerts.html'
    ]
    
    missing_templates = []
    
    for template in required_templates:
        template_path = os.path.join(templates_dir, template)
        if not os.path.exists(template_path):
            missing_templates.append(template)
    
    if missing_templates:
        print("❌ Missing templates:")
        for template in missing_templates:
            print(f"  - {template}")
        return False
    else:
        print("✅ All required templates are present")
        return True

def main():
    print("Verifying Greenhouse Plant Care Application Structure...\n")
    
    checks = [
        verify_project_structure,
        verify_database_schema,
        verify_flask_routes,
        verify_templates
    ]
    
    all_passed = True
    
    for check in checks:
        if not check():
            all_passed = False
        print()
    
    if all_passed:
        print("🎉 All checks passed! The application structure is complete.")
        print("\nTo run the application:")
        print("1. Install MySQL server and create a database")
        print("2. Update config.py with your database credentials")
        print("3. Run: pip install -r requirements.txt")
        print("4. Run: python app.py")
        print("5. Visit: http://localhost:5000")
    else:
        print("❌ Some checks failed. Please review the issues above.")

if __name__ == '__main__':
    main()