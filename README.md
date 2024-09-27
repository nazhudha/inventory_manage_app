Instructions on Running the Application (README)
Running the Application Locally:

1. Clone the repository or extract the zip file

2. Create a virtual environment and install dependencies:

python3 -m venv venv                                            | Create a virtual environment
source venv/bin/activate                                        | Activate the virtual environment 
pip install -U -r requirements.txt                              | Install the updated requirements
pip install Flask Flask-SQLAlchemy Flask-Login Flask-WTF		| install Packages + Flask

3. Set up the SQLite database:

flask db init
flask db migrate
flask db upgrade

4. Run the application:

flask run							    | Run the App 
OR
flask --app run app				        | Run the app, specifying ‘app.py’ file


5. Run unit tests:
python -m unittest tests/test_app.py          | run all tests 
