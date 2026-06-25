from app import app
import unittest

class FlaskTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        
    def test_dashboard_route(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        
    def test_plants_route(self):
        response = self.app.get('/plants')
        self.assertEqual(response.status_code, 200)
        
    def test_add_plant_route(self):
        response = self.app.get('/plants/add')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()