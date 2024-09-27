import unittest
from app import create_app, db
from app.models import User, Equipment
from flask import url_for
from werkzeug.security import generate_password_hash, check_password_hash

class FlaskTestCase(unittest.TestCase):
    def setUp(self):
        """Set up a temporary Flask test environment"""
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # In-memory DB for testing
        self.app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing
        self.app.config['SERVER_NAME'] = 'localhost'
        self.client = self.app.test_client()

        # Create all tables
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        """Tear down the test environment"""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_home_page(self):
        """Test home page loads successfully"""
        response = self.client.get(url_for('main.home'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to Home Page', response.data)

    def test_user_registration(self):
        """Test user registration works correctly"""
        with self.app.app_context():
            response = self.client.post(url_for('main.register'), data={
                'username': 'newuser',
                'email': 'newuser@example.com',
                'password': 'password123',
                'role': 'regular'
            })
            self.assertEqual(response.status_code, 302)

            # Check if user was created in the database
            user = User.query.filter_by(email='newuser@example.com').first()
            self.assertIsNotNone(user)
            self.assertTrue(check_password_hash(user.password, 'password123'))

    def test_user_login(self):
        """Test user login works correctly"""
        with self.app.app_context():
            # Create a test user with hashed password
            hashed_password = generate_password_hash('password123')
            user = User(username='testuser', email='testuser@example.com', password=hashed_password, role='regular')
            db.session.add(user)
            db.session.commit()

            # Attempt login
            response = self.client.post(url_for('main.login'), data={
                'email': 'testuser@example.com',
                'password': 'password123'  # This should match the unhashed password
            })
            self.assertEqual(response.status_code, 302)

    def test_add_equipment(self):
        """Test equipment creation"""
        with self.app.app_context():
            # Check if admin user already exists, or create one
            admin = User.query.filter_by(email='admin@example.com').first()
            if not admin:
                response = self.client.post(url_for('main.register'), data={
                    'username': 'adminuser',
                    'email': 'admin@example.com',
                    'password': 'adminpassword',
                    'role': 'admin'
                })

            # Log in as admin
            self.client.post(url_for('main.login'), data={
                'email': 'admin@example.com',
                'password': 'adminpassword'
            })

            # Add equipment
            response = self.client.post(url_for('main.new_equipment'), data={
                'name': 'Laptop',
                'quantity': 5,
                'user': 1  # Admin user is assigned this equipment
            })
            self.assertEqual(response.status_code, 302)

            # Check if equipment was added
            equipment = Equipment.query.filter_by(name='Laptop').first()
            self.assertIsNotNone(equipment)
            self.assertEqual(equipment.quantity, 5)

    def test_delete_equipment_as_admin(self):
        """Test that admin can delete equipment"""
        with self.app.app_context():
            # Fetch admin if already exists or create a new admin user
            admin = User.query.filter_by(email='admin@example.com').first()
            if not admin:
                hashed_password = generate_password_hash('adminpassword')
                admin = User(username='adminuser', email='admin@example.com', password=hashed_password, role='admin')
                db.session.add(admin)
                db.session.commit()

            # Log in as admin
            self.client.post(url_for('main.login'), data={
                'email': 'admin@example.com',
                'password': 'adminpassword'
            })

            # Create equipment to be deleted
            equipment = Equipment(name='Monitor', quantity=2, user_id=admin.id)
            db.session.add(equipment)
            db.session.commit()

            # Delete equipment
            response = self.client.post(url_for('main.delete_equipment', id=equipment.id))
            self.assertEqual(response.status_code, 302)

            # Verify equipment has been deleted
            deleted_equipment = db.session.get(Equipment, equipment.id)  # Using Session.get instead of Query.get
            self.assertIsNone(deleted_equipment)

if __name__ == '__main__':
    unittest.main()
