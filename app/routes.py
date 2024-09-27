from flask import Blueprint, render_template, flash, redirect, request, url_for
from app.extensions import db 
from app.forms import EquipmentForm, LoginForm, RegistrationForm
from app.models import Equipment, User
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

main = Blueprint('main', __name__)

# Function to create a database connection
def get_db_connection():
    conn = sqlite3.connect('site.db')
    conn.row_factory = sqlite3.Row
    return conn

# Home route
@main.route('/')
def home():
    return render_template('home.html', title='Home')


@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Hash the password
        hashed_password = generate_password_hash(form.password.data)
        
        # Create new user instance
        user = User(
            username=form.username.data, 
            email=form.email.data, 
            password=hashed_password, 
            role=form.role.data
        )
        
        # Add user to the database
        db.session.add(user)
        db.session.commit()
        
        # Flash success message and redirect to login page
        flash('Account created successfully', 'success')
        return redirect(url_for('main.login'))  # Use 'main.login' since it's inside a blueprint
    
    return render_template('register.html', form=form, edirect_to_login=True)

@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Find the user by email
        user = User.query.filter_by(email=form.email.data).first()

        # Check if user exists and the password is correct
        if user and check_password_hash(user.password, form.password.data):  # Correct usage of check_password_hash
            login_user(user)
            flash('Login Successful!', 'success')
            return redirect(url_for('main.dashboard'))  # Use 'main.dashboard'
        else:
            flash('Login Failed. Check email and password', 'danger')
    
    return render_template('login.html', form=form)

@main.route('/dashboard')
@login_required
def dashboard():
    # Get the current page number from the query string (default to 1 if not provided)
    page = request.args.get('page', 1, type=int)

    # Paginate the query for equipment, showing 5 items per page
    equipments = Equipment.query.paginate(page=page, per_page=5)

    return render_template('dashboard.html', equipments=equipments)

@main.route('/equipment/new', methods=['GET', 'POST'])
@login_required
def new_equipment():
    form = EquipmentForm()

    # Admin users can assign equipment to any user
    if current_user.role == 'admin':
        form.user.choices = [(user.id, user.username) for user in User.query.all()]
    else:
        # Remove the user field for regular users
        del form.user

    if form.validate_on_submit():
        # Assign the equipment to the current user by default
        user_id = current_user.id

        # Admin can assign to any user
        if current_user.role == 'admin':
            user_id = form.user.data

        equipment = Equipment(
            name=form.name.data,
            quantity=form.quantity.data,
            user_id=user_id  # Assign to the selected or current user
        )
        db.session.add(equipment)
        db.session.commit()

        flash('New equipment added successfully!', 'success')
        return redirect(url_for('main.dashboard'))

    return render_template('new_equipment.html', form=form)

@main.route('/equipment/delete/<int:id>', methods=['POST'])
@login_required
def delete_equipment(id):
     # Only allow admin to delete
    if current_user.role != 'admin':
        flash('Access Denied Not Admin', 'danger')
        return redirect(url_for('main.dashboard'))

     # Get the equipment by ID and delete it
    equipment = Equipment.query.get_or_404(id)
    db.session.delete(equipment)
    db.session.commit()
    flash(f'{equipment.name} has been deleted.', 'success')
    return redirect(url_for('main.dashboard'))

@main.route('/equipment/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_equipment(id):
    equipment = Equipment.query.get_or_404(id)
    form = EquipmentForm(obj=equipment)

    if current_user.role != 'admin':
        # Regular users can only edit the name and quantity, not the assigned user
        del form.user

    elif form.user:
        # Admin can change the assigned user
        form.user.choices = [(user.id, user.username) for user in User.query.all()]

    if form.validate_on_submit():
        equipment.name = form.name.data
        equipment.quantity = form.quantity.data

        # Only allow admins to update the assigned user
        if current_user.role == 'admin' and 'user' in form:
            equipment.user_id = form.user.data

        db.session.commit()
        flash(f'{equipment.name} has been updated!', 'success')
        return redirect(url_for('main.dashboard'))

    return render_template('edit_equipment.html', form=form)

# Route for displaying the list of users (Admin-only)
@main.route('/users', methods=['GET'])
@login_required
def user_list():
    # Ensure that only admins can access this page
    if current_user.role != 'admin':
        flash('Access Denied: Admins Only!', 'danger')
        return redirect(url_for('main.dashboard'))

    # Fetch all users from the database
    users = User.query.all()

    # Render the user list template
    return render_template('user_list.html', users=users)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('main.login'))

