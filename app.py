from app import app
from app import create_app

app = create_app()

# Initialize the app and run
if __name__ == "__main__":
    app.run(debug=True)

