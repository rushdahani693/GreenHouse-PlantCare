import os

class Config:
    # SQLite configuration
    DATABASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'greenhouse.db')
    
    # Secret key for sessions
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key-here')