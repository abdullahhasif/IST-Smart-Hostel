from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, TextAreaField, IntegerField, FloatField, DateField, BooleanField, HiddenField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError, Optional, NumberRange
from models import User, StudentProfile

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username is already taken. Please choose a different one.')
            
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email is already registered. Please use a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class StudentProfileForm(FlaskForm):
    full_name = StringField('Full Name', validators=[DataRequired(), Length(max=100)])
    roll_number = StringField('Roll Number', validators=[DataRequired(), Length(max=20)])
    contact_number = StringField('Contact Number', validators=[DataRequired(), Length(max=20)])
    address = StringField('Address', validators=[DataRequired(), Length(max=200)])
    department = StringField('Department', validators=[DataRequired(), Length(max=100)])
    semester = IntegerField('Semester', validators=[DataRequired(), NumberRange(min=1, max=12)])
    emergency_contact_name = StringField('Emergency Contact Name', validators=[DataRequired(), Length(max=100)])
    emergency_contact_number = StringField('Emergency Contact Number', validators=[DataRequired(), Length(max=20)])
    submit = SubmitField('Update Profile')
    
    def validate_roll_number(self, roll_number):
        profile = StudentProfile.query.filter_by(roll_number=roll_number.data).first()
        if profile and profile.user_id != self.user_id:
            raise ValidationError('This roll number is already registered.')


class BookingRequestForm(FlaskForm):
    hostel_id = SelectField('Hostel', coerce=int, validators=[DataRequired()])
    room_type = SelectField('Room Type', choices=[
        ('Single', 'Single Room'),
        ('Double', 'Double Room'),
        ('Triple', 'Triple Room')
    ], validators=[DataRequired()])
    start_date = DateField('Start Date', validators=[DataRequired()])
    end_date = DateField('End Date', validators=[DataRequired()])
    special_requests = TextAreaField('Special Requests', validators=[Optional(), Length(max=500)])
    submit = SubmitField('Submit Booking Request')


class ComplaintForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=100)])
    category = SelectField('Category', choices=[
        ('Electrical', 'Electrical'),
        ('Plumbing', 'Plumbing'),
        ('Furniture', 'Furniture'),
        ('Cleanliness', 'Cleanliness'),
        ('Security', 'Security'),
        ('Internet', 'Internet'),
        ('Other', 'Other')
    ], validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired(), Length(max=1000)])
    submit = SubmitField('Submit Complaint')


class VisitorForm(FlaskForm):
    visitor_name = StringField('Visitor Name', validators=[DataRequired(), Length(max=100)])
    visitor_contact = StringField('Visitor Contact', validators=[DataRequired(), Length(max=20)])
    purpose = StringField('Purpose of Visit', validators=[DataRequired(), Length(max=200)])
    visit_date = DateField('Visit Date', validators=[DataRequired()])
    submit = SubmitField('Register Visitor')


class PaymentForm(FlaskForm):
    payment_type = SelectField('Payment Type', choices=[
        ('Hostel Fee', 'Hostel Fee'),
        ('Security Deposit', 'Security Deposit'),
        ('Late Fee', 'Late Fee'),
        ('Other', 'Other')
    ], validators=[DataRequired()])
    amount = FloatField('Amount', validators=[DataRequired(), NumberRange(min=0.01)])
    payment_method = SelectField('Payment Method', choices=[
        ('Cash', 'Cash'),
        ('Bank Transfer', 'Bank Transfer'),
        ('Online Payment', 'Online Payment')
    ], validators=[DataRequired()])
    transaction_id = StringField('Transaction ID', validators=[Optional(), Length(max=100)])
    submit = SubmitField('Submit Payment')


class ApplicationStatusForm(FlaskForm):
    status = SelectField('Status', choices=[
        ('approved', 'Approve'),
        ('rejected', 'Reject')
    ], validators=[DataRequired()])
    admin_notes = TextAreaField('Notes', validators=[Optional(), Length(max=500)])
    submit = SubmitField('Update Status')


class ComplaintStatusForm(FlaskForm):
    status = SelectField('Status', choices=[
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved')
    ], validators=[DataRequired()])
    admin_notes = TextAreaField('Admin Notes', validators=[Optional(), Length(max=500)])
    submit = SubmitField('Update Status')


class RoomForm(FlaskForm):
    room_number = StringField('Room Number', validators=[DataRequired(), Length(max=10)])
    room_type = SelectField('Room Type', choices=[
        ('Single', 'Single Room'),
        ('Double', 'Double Room'),
        ('Triple', 'Triple Room')
    ], validators=[DataRequired()])
    capacity = IntegerField('Capacity', validators=[DataRequired(), NumberRange(min=1, max=10)])
    fee_per_semester = FloatField('Fee per Semester', validators=[DataRequired(), NumberRange(min=0.01)])
    is_available = BooleanField('Is Available')
    hostel_id = SelectField('Hostel', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Submit')


class RoomAllocationForm(FlaskForm):
    application_id = HiddenField('Application ID')
    room_id = SelectField('Room', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Allocate Room')
