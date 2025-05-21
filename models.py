from datetime import datetime
from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='student')  # 'student' or 'admin'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    student_profile = db.relationship('StudentProfile', backref='user', uselist=False, cascade='all, delete-orphan')
    bookings = db.relationship('Booking', backref='user', lazy=True, cascade='all, delete-orphan')
    complaints = db.relationship('Complaint', backref='user', lazy=True, cascade='all, delete-orphan')
    payments = db.relationship('Payment', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'


class Hostel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    
    # Relationships
    rooms = db.relationship('Room', backref='hostel', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Hostel {self.name}>'


class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_number = db.Column(db.String(10), nullable=False)
    room_type = db.Column(db.String(50), nullable=False)  # e.g., Single, Double, etc.
    capacity = db.Column(db.Integer, nullable=False)
    fee_per_semester = db.Column(db.Float, nullable=False)
    is_available = db.Column(db.Boolean, default=True)
    hostel_id = db.Column(db.Integer, db.ForeignKey('hostel.id'), nullable=False)
    
    # Relationships
    bookings = db.relationship('Booking', backref='room', lazy=True)
    
    def __repr__(self):
        return f'<Room {self.room_number} in Hostel {self.hostel_id}>'


class StudentProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    roll_number = db.Column(db.String(20), unique=True, nullable=False)
    contact_number = db.Column(db.String(20))
    address = db.Column(db.String(200))
    department = db.Column(db.String(100))
    semester = db.Column(db.Integer)
    emergency_contact_name = db.Column(db.String(100))
    emergency_contact_number = db.Column(db.String(20))
    
    def __repr__(self):
        return f'<StudentProfile {self.full_name}>'


class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, approved, rejected, completed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Booking {self.id} by User {self.user_id}>'


class Complaint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50))  # e.g., Electrical, Plumbing, Furniture, etc.
    status = db.Column(db.String(20), default='open')  # open, in_progress, resolved
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    admin_notes = db.Column(db.Text)
    
    def __repr__(self):
        return f'<Complaint {self.id} by User {self.user_id}>'


class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payment_type = db.Column(db.String(50), nullable=False)  # e.g., Hostel Fee, Security Deposit, etc.
    payment_method = db.Column(db.String(50))  # e.g., Cash, Bank Transfer, etc.
    transaction_id = db.Column(db.String(100), unique=True)
    status = db.Column(db.String(20), default='pending')  # pending, completed, failed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Payment {self.id} by User {self.user_id}>'


class Visitor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    visitor_name = db.Column(db.String(100), nullable=False)
    visitor_contact = db.Column(db.String(20))
    purpose = db.Column(db.String(200))
    visit_date = db.Column(db.Date, nullable=False)
    check_in_time = db.Column(db.Time)
    check_out_time = db.Column(db.Time)
    status = db.Column(db.String(20), default='scheduled')  # scheduled, checked_in, checked_out, cancelled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Visitor {self.visitor_name} to Student {self.student_id}>'


class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    hostel_id = db.Column(db.Integer, db.ForeignKey('hostel.id'), nullable=False)
    semester = db.Column(db.Integer, nullable=False)
    room_preference = db.Column(db.String(50))
    special_requirements = db.Column(db.Text)
    status = db.Column(db.String(20), default='pending')  # pending, approved, rejected
    admin_notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref=db.backref('applications', lazy=True))
    hostel = db.relationship('Hostel', backref=db.backref('applications', lazy=True))
    
    def __repr__(self):
        return f'<Application {self.id} by User {self.user_id}>'
