import unittest
from app import app, db
from models.user import User

class DatabaseTestCase(unittest.TestCase):
    def setUp(self):
        """Set up test database"""
        self.app = app.test_client()
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_database.db'
        app.config['TESTING'] = True
        with app.app_context():
            db.create_all()

    def tearDown(self):
        """Clean up test database"""
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_database_creation(self):
        """Test if the database and table are created successfully"""
        with app.app_context():
            user_count = User.query.count()
            self.assertEqual(user_count, 0)

    def test_add_user(self):
        """Test adding a user to the database"""
        with app.app_context():
            new_user = User(name='Test User', email='test@example.com')
            db.session.add(new_user)
            db.session.commit()
            user = User.query.filter_by(email='test@example.com').first()
            self.assertIsNotNone(user)
            self.assertEqual(user.name, 'Test User')

if __name__ == "__main__":
    unittest.main()