import os
from datetime import datetime, date
from flask import render_template, redirect, url_for, flash, request, jsonify, abort
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.security import generate_password_hash
from sqlalchemy import func

from app import app, db
from models import User, StudentProfile, Hostel, Room, Booking, Complaint, Payment, Visitor, Application
from forms import (
    RegistrationForm, LoginForm, StudentProfileForm, BookingRequestForm,
    ComplaintForm, VisitorForm, PaymentForm, ApplicationStatusForm,
    ComplaintStatusForm, RoomForm, RoomAllocationForm
)
from utils import admin_required

# Home route
@app.route('/')
def index():
    return render_template('index.html')

# Authentication routes
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            role='student'  # Default role is student
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        
        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.role == 'admin':
            return redirect(url_for('admin_dashboard'))
        else:
            return redirect(url_for('student_dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            flash('Login successful!', 'success')
            
            if user.role == 'admin':
                return redirect(next_page or url_for('admin_dashboard'))
            else:
                # Check if profile exists
                if not user.student_profile:
                    return redirect(url_for('student_profile'))
                return redirect(next_page or url_for('student_dashboard'))
        else:
            flash('Login unsuccessful. Please check email and password.', 'danger')
    
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

# Student routes
@app.route('/student/dashboard')
@login_required
def student_dashboard():
    if current_user.role != 'student':
        flash('Access denied.', 'danger')
        return redirect(url_for('index'))
    
    # Get active booking
    active_booking = Booking.query.filter_by(
        user_id=current_user.id, 
        status='approved'
    ).order_by(Booking.created_at.desc()).first()
    
    # Get recent complaints
    recent_complaints = Complaint.query.filter_by(
        user_id=current_user.id
    ).order_by(Complaint.created_at.desc()).limit(5).all()
    
    # Get recent payments
    recent_payments = Payment.query.filter_by(
        user_id=current_user.id
    ).order_by(Payment.created_at.desc()).limit(3).all()
    
    # Check if hostel application exists
    pending_application = Application.query.filter_by(
        user_id=current_user.id,
        status='pending'
    ).first()
    
    return render_template(
        'student/dashboard.html',
        active_booking=active_booking,
        recent_complaints=recent_complaints,
        recent_payments=recent_payments,
        pending_application=pending_application
    )

@app.route('/student/profile', methods=['GET', 'POST'])
@login_required
def student_profile():
    if current_user.role != 'student':
        flash('Access denied.', 'danger')
        return redirect(url_for('index'))
    
    profile = current_user.student_profile
    
    form = StudentProfileForm()
    # Set the user_id for validation
    form.user_id = current_user.id
    
    if form.validate_on_submit():
        if not profile:
            profile = StudentProfile(user_id=current_user.id)
            db.session.add(profile)
        
        profile.full_name = form.full_name.data
        profile.roll_number = form.roll_number.data
        profile.contact_number = form.contact_number.data
        profile.address = form.address.data
        profile.department = form.department.data
        profile.semester = form.semester.data
        profile.emergency_contact_name = form.emergency_contact_name.data
        profile.emergency_contact_number = form.emergency_contact_number.data
        
        db.session.commit()
        flash('Your profile has been updated!', 'success')
        return redirect(url_for('student_dashboard'))
    
    if profile:
        form.full_name.data = profile.full_name
        form.roll_number.data = profile.roll_number
        form.contact_number.data = profile.contact_number
        form.address.data = profile.address
        form.department.data = profile.department
        form.semester.data = profile.semester
        form.emergency_contact_name.data = profile.emergency_contact_name
        form.emergency_contact_number.data = profile.emergency_contact_number
    
    return render_template('student/profile.html', form=form)

@app.route('/student/booking', methods=['GET', 'POST'])
@login_required
def student_booking():
    if current_user.role != 'student':
        flash('Access denied.', 'danger')
        return redirect(url_for('index'))
    
    # Check if student has a profile
    if not current_user.student_profile:
        flash('Please complete your profile before booking a room.', 'warning')
        return redirect(url_for('student_profile'))
    
    # Check if there's an active application
    active_application = Application.query.filter_by(
        user_id=current_user.id
    ).filter(Application.status.in_(['pending', 'approved'])).first()
    
    # Check if there's an active booking
    active_booking = Booking.query.filter_by(
        user_id=current_user.id
    ).filter(Booking.status.in_(['pending', 'approved'])).first()
    
    # If already has active application or booking
    if active_application or active_booking:
        return render_template(
            'student/booking.html',
            active_application=active_application,
            active_booking=active_booking
        )
    
    # Prepare form for new application
    form = BookingRequestForm()
    
    # Get all hostels for dropdown
    hostels = Hostel.query.all()
    form.hostel_id.choices = [(h.id, h.name) for h in hostels]
    
    if form.validate_on_submit():
        # Create new application
        application = Application(
            user_id=current_user.id,
            hostel_id=form.hostel_id.data,
            semester=current_user.student_profile.semester,
            room_preference=form.room_type.data,
            special_requirements=form.special_requests.data,
            status='pending'
        )
        db.session.add(application)
        db.session.commit()
        
        flash('Your hostel application has been submitted!', 'success')
        return redirect(url_for('student_booking'))
    
    return render_template('student/booking.html', form=form)

@app.route('/student/complaints', methods=['GET', 'POST'])
@login_required
def student_complaints():
    if current_user.role != 'student':
        flash('Access denied.', 'danger')
        return redirect(url_for('index'))
    
    # Get all complaints by this student
    complaints = Complaint.query.filter_by(user_id=current_user.id).order_by(Complaint.created_at.desc()).all()
    
    # Prepare form for new complaint
    form = ComplaintForm()
    
    if form.validate_on_submit():
        complaint = Complaint(
            user_id=current_user.id,
            title=form.title.data,
            description=form.description.data,
            category=form.category.data
        )
        db.session.add(complaint)
        db.session.commit()
        
        flash('Your complaint has been submitted!', 'success')
        return redirect(url_for('student_complaints'))
    
    return render_template('student/complaints.html', form=form, complaints=complaints)

@app.route('/student/payment', methods=['GET', 'POST'])
@login_required
def student_payment():
    if current_user.role != 'student':
        flash('Access denied.', 'danger')
        return redirect(url_for('index'))
    
    # Get all payments by this student
    payments = Payment.query.filter_by(user_id=current_user.id).order_by(Payment.created_at.desc()).all()
    
    # Calculate total paid and pending
    total_paid = sum(p.amount for p in payments if p.status == 'completed')
    total_pending = sum(p.amount for p in payments if p.status == 'pending')
    
    # Prepare form for new payment
    form = PaymentForm()
    
    if form.validate_on_submit():
        payment = Payment(
            user_id=current_user.id,
            amount=form.amount.data,
            payment_type=form.payment_type.data,
            payment_method=form.payment_method.data,
            transaction_id=form.transaction_id.data,
            status='pending'  # Initial status is pending until confirmed by admin
        )
        db.session.add(payment)
        db.session.commit()
        
        flash('Your payment has been recorded and is pending verification!', 'success')
        return redirect(url_for('student_payment'))
    
    return render_template(
        'student/payment.html', 
        form=form, 
        payments=payments,
        total_paid=total_paid,
        total_pending=total_pending
    )

@app.route('/student/history')
@login_required
def student_history():
    if current_user.role != 'student':
        flash('Access denied.', 'danger')
        return redirect(url_for('index'))
    
    # Get booking history
    bookings = Booking.query.filter_by(user_id=current_user.id).order_by(Booking.created_at.desc()).all()
    
    # Get application history
    applications = Application.query.filter_by(user_id=current_user.id).order_by(Application.created_at.desc()).all()
    
    return render_template(
        'student/history.html',
        bookings=bookings,
        applications=applications
    )

# Admin routes
@app.route('/admin/dashboard')
@login_required
@admin_required
def admin_dashboard():
    # Count statistics
    total_students = User.query.filter_by(role='student').count()
    total_rooms = Room.query.count()
    vacant_rooms = Room.query.filter_by(is_available=True).count()
    pending_applications = Application.query.filter_by(status='pending').count()
    open_complaints = Complaint.query.filter_by(status='open').count()
    
    # Recent applications
    recent_applications = Application.query.filter_by(status='pending').order_by(Application.created_at.desc()).limit(5).all()
    
    # Recent complaints
    recent_complaints = Complaint.query.filter_by(status='open').order_by(Complaint.created_at.desc()).limit(5).all()
    
    return render_template(
        'admin/dashboard.html',
        total_students=total_students,
        total_rooms=total_rooms,
        vacant_rooms=vacant_rooms,
        pending_applications=pending_applications,
        open_complaints=open_complaints,
        recent_applications=recent_applications,
        recent_complaints=recent_complaints
    )

@app.route('/admin/applications')
@login_required
@admin_required
def admin_applications():
    # Get all applications
    applications = Application.query.order_by(Application.created_at.desc()).all()
    
    return render_template('admin/applications.html', applications=applications)

@app.route('/admin/application/<int:application_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_application_detail(application_id):
    application = Application.query.get_or_404(application_id)
    
    # Get student profile
    student = User.query.get(application.user_id)
    profile = student.student_profile
    
    # Prepare form for status update
    status_form = ApplicationStatusForm()
    
    # If application is approved, prepare room allocation form
    allocation_form = None
    if application.status == 'approved':
        allocation_form = RoomAllocationForm()
        # Get available rooms in the hostel
        available_rooms = Room.query.filter_by(
            hostel_id=application.hostel_id,
            is_available=True,
            room_type=application.room_preference
        ).all()
        allocation_form.room_id.choices = [(r.id, f'{r.room_number} - {r.room_type}') for r in available_rooms]
        allocation_form.application_id.data = application.id
    
    if status_form.validate_on_submit():
        application.status = status_form.status.data
        application.admin_notes = status_form.admin_notes.data
        db.session.commit()
        
        flash(f'Application status updated to {status_form.status.data}!', 'success')
        return redirect(url_for('admin_applications'))
    
    if allocation_form and request.form.get('submit') == 'Allocate Room':
        if allocation_form.validate_on_submit():
            room = Room.query.get(allocation_form.room_id.data)
            if room and room.is_available:
                # Create a new booking
                booking = Booking(
                    user_id=application.user_id,
                    room_id=room.id,
                    start_date=date.today(),  # Use current date as start
                    end_date=date(date.today().year, 12, 31),  # End of semester/year
                    status='approved'
                )
                db.session.add(booking)
                
                # Update room availability
                room.is_available = False
                
                db.session.commit()
                
                flash('Room allocated successfully!', 'success')
                return redirect(url_for('admin_applications'))
    
    return render_template(
        'admin/application_detail.html',
        application=application,
        student=student,
        profile=profile,
        status_form=status_form,
        allocation_form=allocation_form
    )

@app.route('/admin/rooms')
@login_required
@admin_required
def admin_rooms():
    # Get all hostels and rooms
    hostels = Hostel.query.all()
    
    # Get total rooms count
    total_rooms = Room.query.count()
    available_rooms = Room.query.filter_by(is_available=True).count()
    
    return render_template('admin/rooms.html', 
                          hostels=hostels, 
                          total_rooms=total_rooms,
                          available_rooms=available_rooms)

@app.route('/admin/rooms/<int:hostel_id>')
@login_required
@admin_required
def admin_hostel_rooms(hostel_id):
    hostel = Hostel.query.get_or_404(hostel_id)
    rooms = Room.query.filter_by(hostel_id=hostel_id).all()
    
    return render_template('admin/hostel_rooms.html', hostel=hostel, rooms=rooms)

@app.route('/admin/room/add', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_add_room():
    form = RoomForm()
    
    # Get all hostels for dropdown
    hostels = Hostel.query.all()
    form.hostel_id.choices = [(h.id, h.name) for h in hostels]
    
    if form.validate_on_submit():
        room = Room(
            room_number=form.room_number.data,
            room_type=form.room_type.data,
            capacity=form.capacity.data,
            fee_per_semester=form.fee_per_semester.data,
            is_available=form.is_available.data,
            hostel_id=form.hostel_id.data
        )
        db.session.add(room)
        db.session.commit()
        
        flash('Room added successfully!', 'success')
        return redirect(url_for('admin_hostel_rooms', hostel_id=form.hostel_id.data))
    
    return render_template('admin/room_form.html', form=form, title='Add Room')

@app.route('/admin/room/edit/<int:room_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_edit_room(room_id):
    room = Room.query.get_or_404(room_id)
    form = RoomForm()
    
    # Get all hostels for dropdown
    hostels = Hostel.query.all()
    form.hostel_id.choices = [(h.id, h.name) for h in hostels]
    
    if form.validate_on_submit():
        room.room_number = form.room_number.data
        room.room_type = form.room_type.data
        room.capacity = form.capacity.data
        room.fee_per_semester = form.fee_per_semester.data
        room.is_available = form.is_available.data
        room.hostel_id = form.hostel_id.data
        
        db.session.commit()
        
        flash('Room updated successfully!', 'success')
        return redirect(url_for('admin_hostel_rooms', hostel_id=room.hostel_id))
    
    # Pre-populate form
    form.room_number.data = room.room_number
    form.room_type.data = room.room_type
    form.capacity.data = room.capacity
    form.fee_per_semester.data = room.fee_per_semester
    form.is_available.data = room.is_available
    form.hostel_id.data = room.hostel_id
    
    return render_template('admin/room_form.html', form=form, title='Edit Room')

@app.route('/admin/complaints')
@login_required
@admin_required
def admin_complaints():
    # Get all complaints
    complaints = Complaint.query.order_by(Complaint.created_at.desc()).all()
    
    return render_template('admin/complaints.html', complaints=complaints)

@app.route('/admin/complaint/<int:complaint_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_complaint_detail(complaint_id):
    complaint = Complaint.query.get_or_404(complaint_id)
    
    # Get student info
    student = User.query.get(complaint.user_id)
    
    # Prepare form for status update
    form = ComplaintStatusForm()
    
    if form.validate_on_submit():
        complaint.status = form.status.data
        complaint.admin_notes = form.admin_notes.data
        complaint.updated_at = datetime.utcnow()
        db.session.commit()
        
        flash(f'Complaint status updated to {form.status.data}!', 'success')
        return redirect(url_for('admin_complaints'))
    
    # Pre-populate form
    form.status.data = complaint.status
    form.admin_notes.data = complaint.admin_notes
    
    return render_template(
        'admin/complaint_detail.html',
        complaint=complaint,
        student=student,
        form=form
    )

@app.route('/admin/payments')
@login_required
@admin_required
def admin_payments():
    # Get all payments
    payments = Payment.query.order_by(Payment.created_at.desc()).all()
    
    return render_template('admin/payments.html', payments=payments)

@app.route('/admin/payment/<int:payment_id>/update-status/<status>')
@login_required
@admin_required
def admin_update_payment_status(payment_id, status):
    if status not in ['pending', 'completed', 'failed']:
        abort(400)
    
    payment = Payment.query.get_or_404(payment_id)
    payment.status = status
    db.session.commit()
    
    flash(f'Payment status updated to {status}!', 'success')
    return redirect(url_for('admin_payments'))

@app.route('/admin/stats')
@login_required
@admin_required
def admin_stats():
    # Student statistics
    total_students = User.query.filter_by(role='student').count()
    students_with_booking = db.session.query(func.count(func.distinct(Booking.user_id))).filter(Booking.status == 'approved').scalar()
    students_percentage = (students_with_booking / total_students * 100) if total_students > 0 else 0
    
    # Room statistics
    total_rooms = Room.query.count()
    occupied_rooms = Room.query.filter_by(is_available=False).count()
    vacancy_percentage = ((total_rooms - occupied_rooms) / total_rooms * 100) if total_rooms > 0 else 0
    
    # Complaint statistics
    total_complaints = Complaint.query.count()
    open_complaints = Complaint.query.filter_by(status='open').count()
    in_progress_complaints = Complaint.query.filter_by(status='in_progress').count()
    resolved_complaints = Complaint.query.filter_by(status='resolved').count()
    
    # Payment statistics
    total_payments = Payment.query.filter_by(status='completed').count()
    total_amount = db.session.query(func.sum(Payment.amount)).filter(Payment.status == 'completed').scalar() or 0
    
    # Hostel occupancy
    hostels = Hostel.query.all()
    hostel_stats = []
    
    for hostel in hostels:
        total_hostel_rooms = Room.query.filter_by(hostel_id=hostel.id).count()
        occupied_hostel_rooms = Room.query.filter_by(hostel_id=hostel.id, is_available=False).count()
        occupancy_percentage = (occupied_hostel_rooms / total_hostel_rooms * 100) if total_hostel_rooms > 0 else 0
        
        hostel_stats.append({
            'name': hostel.name,
            'total_rooms': total_hostel_rooms,
            'occupied_rooms': occupied_hostel_rooms,
            'occupancy_percentage': occupancy_percentage
        })
    
    return render_template(
        'admin/stats.html',
        total_students=total_students,
        students_with_booking=students_with_booking,
        students_percentage=students_percentage,
        total_rooms=total_rooms,
        occupied_rooms=occupied_rooms,
        vacancy_percentage=vacancy_percentage,
        total_complaints=total_complaints,
        open_complaints=open_complaints,
        in_progress_complaints=in_progress_complaints,
        resolved_complaints=resolved_complaints,
        total_payments=total_payments,
        total_amount=total_amount,
        hostel_stats=hostel_stats
    )

# Utility routes
@app.route('/init-db')
def init_db():
    # Only use this in development
    if not app.debug:
        return "Not allowed in production", 403
    
    # Create admin user if doesn't exist
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(
            username='admin',
            email='admin@ist.edu',
            role='admin'
        )
        admin.set_password('admin123')  # Default password, should be changed
        db.session.add(admin)
    
    # Create default hostels if don't exist
    hostels = [
        {'name': 'Hostel-I', 'address': 'IST Campus, Islamabad', 'description': 'Main hostel building for male students'},
        {'name': 'Hostel-II', 'address': 'IST Campus, Islamabad', 'description': 'Secondary hostel building for male students'},
        {'name': 'Hostel-III', 'address': 'IST Campus, Islamabad', 'description': 'Hostel building for female students'}
    ]
    
    for hostel_data in hostels:
        hostel = Hostel.query.filter_by(name=hostel_data['name']).first()
        if not hostel:
            hostel = Hostel(**hostel_data)
            db.session.add(hostel)
    
    db.session.commit()
    
    flash('Database initialized with default data!', 'success')
    return redirect(url_for('index'))

# API routes (for AJAX and charts)
@app.route('/api/room-stats')
@login_required
@admin_required
def api_room_stats():
    # Room statistics by type
    room_types = db.session.query(Room.room_type, func.count(Room.id)).group_by(Room.room_type).all()
    room_type_data = {
        'labels': [r[0] for r in room_types],
        'data': [r[1] for r in room_types]
    }
    
    # Room availability
    available_rooms = Room.query.filter_by(is_available=True).count()
    occupied_rooms = Room.query.filter_by(is_available=False).count()
    availability_data = {
        'labels': ['Available', 'Occupied'],
        'data': [available_rooms, occupied_rooms]
    }
    
    return jsonify({
        'room_types': room_type_data,
        'availability': availability_data
    })

@app.route('/api/complaint-stats')
@login_required
@admin_required
def api_complaint_stats():
    # Complaint statistics by status
    status_counts = db.session.query(Complaint.status, func.count(Complaint.id)).group_by(Complaint.status).all()
    status_data = {
        'labels': [s[0].replace('_', ' ').capitalize() for s in status_counts],
        'data': [s[1] for s in status_counts]
    }
    
    # Complaint statistics by category
    category_counts = db.session.query(Complaint.category, func.count(Complaint.id)).group_by(Complaint.category).all()
    category_data = {
        'labels': [c[0] for c in category_counts],
        'data': [c[1] for c in category_counts]
    }
    
    return jsonify({
        'status': status_data,
        'category': category_data
    })

@app.route('/api/hostel-stats')
@login_required
@admin_required
def api_hostel_stats():
    hostels = Hostel.query.all()
    labels = []
    occupied_data = []
    available_data = []
    
    for hostel in hostels:
        labels.append(hostel.name)
        occupied = Room.query.filter_by(hostel_id=hostel.id, is_available=False).count()
        available = Room.query.filter_by(hostel_id=hostel.id, is_available=True).count()
        
        occupied_data.append(occupied)
        available_data.append(available)
    
    return jsonify({
        'labels': labels,
        'occupied': occupied_data,
        'available': available_data
    })
