from flask import Flask
from app.extensions import db, login_manager  # Import db and login_manager from extensions
from app import models
from app.routes import main  # Import the Blueprint
from app.extensions import db
from app.seed_data import seed_equipment_data, seed_user_data


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # Initialize the extensions with the app
    db.init_app(app)
    login_manager.init_app(app)

    login_manager.login_view = 'main.login'

    @login_manager.user_loader
    def load_user(user_id):
        return models.User.query.get(int(user_id))

    # Register the Blueprint
    app.register_blueprint(main)
    
    # Database initialization
    with app.app_context():
        db.drop_all()
        db.create_all()  # This will create all tables based on models if they don't exist
        
        # Seed the database with prefilled data
        seed_user_data()
        seed_equipment_data()
    
    return app

