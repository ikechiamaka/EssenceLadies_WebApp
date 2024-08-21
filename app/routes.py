# app/routes.py
from flask import render_template, url_for, flash, redirect, request
from app import app, db, bcrypt
from app.forms import RegistrationForm, LoginForm, ProfileForm
from app.models import User, Profile
from flask_login import login_user, current_user, logout_user, login_required
from flask import request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os
from app import db, bcrypt
from app.models import User
from app.models import Profile
import uuid
import logging
from flask import render_template, flash, redirect, url_for, request, current_app
from flask_login import login_required
from app.forms import ProfileForm
from app.models import User, Profile, Booking  # Ensure Booking is included here
import csv
from flask import send_file

logging.basicConfig(level=logging.DEBUG)


# UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER




@app.route('/')
def index():
    profiles = Profile.query.all()
    return render_template('index.html', profiles=profiles)

# @app.route('/profile/<int:profile_id>')
# def profile(profile_id):
#     profile = Profile.query.get_or_404(profile_id)
#     return render_template('profile.html', profile=profile)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)





@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin_dashboard'))
    
    form = LoginForm()
    
    if form.validate_on_submit():
        # Authenticate using username only
        user = User.query.filter_by(username=form.username.data).first()
        
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    
    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))






def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS





from flask_login import current_user

@app.route('/new_profile', methods=['GET', 'POST'])
@login_required
def new_profile():
    form = ProfileForm()
    if form.validate_on_submit():
        file = form.profile_picture.data
        filename = secure_filename(file.filename)

        # Ensure the upload directory exists
        upload_dir = current_app.config['UPLOAD_FOLDER']
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)

        file_path = os.path.join(upload_dir, filename)
        file.save(file_path)

        # Create a new profile with the current user's ID as the owner_id
        new_profile = Profile(
            name=form.name.data,
            description=form.description.data,
            age=form.age.data,
            nationality=form.nationality.data,
            height=form.height.data,
            stats=form.stats.data,
            dress_size=form.dress_size.data,
            hair_color=form.hair_color.data,
            eye_color=form.eye_color.data,
            service_level=form.service_level.data,
            languages=form.languages.data,
            bisexual=form.bisexual.data,
            incall_location=form.incall_location.data,
            outcall_location=form.outcall_location.data,
            profile_picture=filename,
            owner_id=current_user.id  # Set the owner_id to the current user's ID
        )

        db.session.add(new_profile)
        db.session.commit()

        flash('Profile successfully created!', 'success')
        return redirect(url_for('index'))
    return render_template('create_profile.html', form=form)






@app.route('/delete_profiles', methods=['GET', 'POST'])
@login_required
def delete_profiles():
    if not current_user.is_admin:
        flash('You do not have permission to perform this action', 'danger')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        selected_profiles = request.form.getlist('profiles')
        if selected_profiles:
            try:
                for profile_id in selected_profiles:
                    profile = Profile.query.get(int(profile_id))
                    if profile:
                        db.session.delete(profile)
                db.session.commit()
                flash('Selected profiles have been deleted', 'success')
            except Exception as e:
                db.session.rollback()
                flash(f'Error deleting profiles: {str(e)}', 'danger')
        else:
            flash('No profiles were selected for deletion', 'warning')
    
    profiles = Profile.query.all()
    return render_template('delete_profiles.html', profiles=profiles)






@app.route('/create_admin')
def create_admin():
    admin_username = 'admin'
    admin_email = 'admin@example.com'
    admin_password = '1234'

    # Check if the admin user already exists
    existing_user = User.query.filter_by(username=admin_username).first()
    if existing_user:
        return "Admin user already exists!"

    # Hash the password
    hashed_password = bcrypt.generate_password_hash(admin_password).decode('utf-8')

    # Create the admin user
    admin_user = User(username=admin_username, email=admin_email, password=hashed_password, is_admin=True)

    # Add the user to the database
    db.session.add(admin_user)
    db.session.commit()

    return f"Admin user {admin_username} created successfully!"



@app.route('/admin_dashboard')
# @login_required
def admin_dashboard():
    # if not current_user.is_admin:
    #     flash('You do not have permission to access this page', 'danger')
    #     return redirect(url_for('index'))
    return render_template('admin_dashboard.html')


@app.route('/reset_password')
def reset_password():
    # Placeholder for password reset functionality
    return render_template('reset_password.html')


@app.route('/escorts')
def escorts():
    profiles = Profile.query.all()
    return render_template('escorts.html', profiles=profiles)

@app.route('/profile/<int:profile_id>')
def profile(profile_id):
    profile = Profile.query.get_or_404(profile_id)
    return render_template('profile.html', profile=profile)


@app.route('/select_escorts_tonight', methods=['GET', 'POST'])
@login_required
def select_escorts_tonight():
    if not current_user.is_admin:
        flash('You do not have permission to perform this action', 'danger')
        return redirect(url_for('index'))

    if request.method == 'POST':
        selected_profiles = request.form.getlist('profiles')
        try:
            # Clear all tonight flags first
            Profile.query.update({Profile.tonight: False})
            db.session.commit()

            # Set tonight flag for selected profiles
            for profile_id in selected_profiles:
                profile = Profile.query.get(int(profile_id))
                if profile:
                    profile.tonight = True
            db.session.commit()

            flash('Escorts Tonight have been updated', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating Escorts Tonight: {str(e)}', 'danger')

    profiles = Profile.query.all()
    return render_template('select_escorts_tonight.html', profiles=profiles)

@app.route('/escorts_tonight')
def escorts_tonight():
    profiles = Profile.query.filter_by(tonight=True).all()
    return render_template('escorts_tonight.html', profiles=profiles)


@app.route('/bookings')
def bookings():
    return render_template('bookings.html')


from datetime import datetime

@app.route('/make_booking', methods=['POST'])
def make_booking():
    print(request.form)  # This will print the form data to the console
    escort_name = request.form['escort_name']
    telephone = request.form['telephone']
    time_to_call = request.form['time_to_call']
    email = request.form['email']
    location = request.form['location']
    length_of_booking = request.form['length']
    date_str = request.form['date']  # Get the date string
    details = request.form['details']

    # Convert the date string to a Python date object
    date_of_booking = datetime.strptime(date_str, '%Y-%m-%d').date()

    booking = Booking(
        escort_name=escort_name,
        telephone=telephone,
        time_to_call=time_to_call,
        email=email,
        location=location,
        length_of_booking=length_of_booking,
        date_of_booking=date_of_booking,  # Use the converted date object
        additional_details=details
    )
    db.session.add(booking)
    db.session.commit()

    flash('Booking has been made successfully!', 'success')
    return redirect(url_for('bookings'))


@app.route('/view_bookings')
@login_required
def view_bookings():
    if not current_user.is_admin:
        flash('You do not have permission to perform this action', 'danger')
        return redirect(url_for('index'))

    bookings = Booking.query.all()
    return render_template('view_bookings.html', bookings=bookings)

@app.route('/clear_bookings', methods=['POST'])
@login_required
def clear_bookings():
    if not current_user.is_admin:
        flash('You do not have permission to perform this action', 'danger')
        return redirect(url_for('index'))
    
    try:
        Booking.query.delete()
        db.session.commit()
        flash('All bookings have been cleared', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error clearing bookings: {str(e)}', 'danger')
    
    return redirect(url_for('view_bookings'))

import os

@app.route('/export_bookings')
@login_required
def export_bookings():
    if not current_user.is_admin:
        flash('You do not have permission to perform this action', 'danger')
        return redirect(url_for('index'))

    # Path to save the CSV file
    csv_file_path = os.path.join(app.root_path, 'bookings.csv')

    # Create the CSV file
    with open(csv_file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Escort Name', 'Telephone', 'Time to Call', 'Email', 'Location', 'Length of Booking', 'Date of Booking', 'Additional Details'])
        bookings = Booking.query.all()
        for booking in bookings:
            writer.writerow([booking.escort_name, booking.telephone, booking.time_to_call, booking.email, booking.location, booking.length_of_booking, booking.date_of_booking, booking.additional_details])

    # Send the file for download
    return send_file(csv_file_path, as_attachment=True, download_name='bookings.csv')

@app.route('/prices')
def prices():
    return render_template('prices.html')

@app.route('/recruitment')
def recruitment():
    return render_template('recruitment.html')
