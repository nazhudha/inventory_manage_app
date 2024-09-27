from app.extensions import db  # Import db and login_manager from extensions
from werkzeug.security import generate_password_hash
from app.models import Equipment, User
from app.extensions import db


# Prefill the Databse with some users
def seed_user_data():
     # Check if any users already exist
    if User.query.first():
        print("Database already has users, skipping seeding.")
        return
    
    # Create an admin user
    admin_user = User(
        username='admin',
        email='admin@example.com',
        password=generate_password_hash('adminpassword'),  # Hashed password
        role='admin'
    )

    # Create two regular users
    regular_user_1 = User(
        username='regular1',
        email='regular1@example.com',
        password=generate_password_hash('password123'),  # Hashed password
        role='regular'
    )

    regular_user_2 = User(
        username='regular2',
        email='regular2@example.com',
        password=generate_password_hash('password123'),  # Hashed password
        role='regular'
    )

    # Add users to the session and commit to the database
    db.session.add(admin_user)
    db.session.add(regular_user_1)
    db.session.add(regular_user_2)
    db.session.commit()

    print('Database seeded with 1 admin and 2 regular users')
        

def seed_equipment_data():
    regular_user_1 = User.query.filter_by(username='regular1').first()
    regular_user_2 = User.query.filter_by(username='regular2').first()

    equipments = [
        {'name': 'Laptop', 'quantity': 10, 'user_id': regular_user_1.id},
        {'name': 'Monitor', 'quantity': 5, 'user_id': regular_user_1.id},
        {'name': 'Keyboard', 'quantity': 7, 'user_id': regular_user_2.id},
        {'name': 'Mouse', 'quantity': 3, 'user_id': regular_user_2.id},
        {'name': 'Printer', 'quantity': 2, 'user_id': regular_user_1.id},
        {'name': 'Scanner', 'quantity': 1, 'user_id': regular_user_1.id},
        {'name': 'Desk', 'quantity': 4, 'user_id': regular_user_2.id},
        {'name': 'Chair', 'quantity': 6, 'user_id': regular_user_2.id},
        {'name': 'Router', 'quantity': 2, 'user_id': regular_user_1.id},
        {'name': 'Switch', 'quantity': 8, 'user_id': regular_user_2.id},
    ]

    for equipment_data in equipments:
        equipment = Equipment(
            name=equipment_data['name'],
            quantity=equipment_data['quantity'],
            user_id=equipment_data['user_id']
        )
        db.session.add(equipment)

    db.session.commit()
    print('Seeded 10 equipment items')
    
