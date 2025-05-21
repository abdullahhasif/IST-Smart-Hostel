from app import app, db
from models import User, Hostel, Room
from werkzeug.security import generate_password_hash

def init_database():
    with app.app_context():
        print("Creating initial database records...")
        
        # Create admin user
        admin_exists = User.query.filter_by(email='admin@example.com').first()
        if not admin_exists:
            admin = User(
                username='admin',
                email='admin@example.com',
                password_hash=generate_password_hash('admin123'),
                role='admin'
            )
            db.session.add(admin)
            print("Admin user created")
        
        # Create demo student user
        student_exists = User.query.filter_by(email='student@example.com').first()
        if not student_exists:
            student = User(
                username='student',
                email='student@example.com',
                password_hash=generate_password_hash('student123'),
                role='student'
            )
            db.session.add(student)
            print("Student user created")
        
        # Create hostels
        hostel_names = ['Hostel-I', 'Hostel-II', 'Hostel-III']
        for i, name in enumerate(hostel_names):
            hostel_exists = Hostel.query.filter_by(name=name).first()
            if not hostel_exists:
                hostel = Hostel(
                    name=name,
                    address=f'Campus Area Block {i+1}, IST',
                    description=f'Modern {name} with all facilities including Wi-Fi, laundry, and common room.'
                )
                db.session.add(hostel)
                print(f"Hostel {name} created")
        
        # Commit changes
        db.session.commit()
        
        # Add rooms to each hostel
        hostels = Hostel.query.all()
        room_types = ['Single', 'Double', 'Triple']
        capacities = [1, 2, 3]
        fees = [50000, 35000, 25000]
        
        for hostel in hostels:
            # Check if hostel already has rooms
            existing_rooms = Room.query.filter_by(hostel_id=hostel.id).count()
            if existing_rooms == 0:
                for floor in range(1, 4):  # 3 floors
                    for room_num in range(1, 11):  # 10 rooms per floor
                        room_type_index = (floor + room_num) % 3
                        room = Room(
                            room_number=f'{floor}0{room_num}',
                            room_type=room_types[room_type_index],
                            capacity=capacities[room_type_index],
                            fee_per_semester=fees[room_type_index],
                            is_available=True,
                            hostel_id=hostel.id
                        )
                        db.session.add(room)
                print(f"Added rooms to {hostel.name}")
        
        # Commit changes
        db.session.commit()
        print("Database initialization completed successfully!")

if __name__ == '__main__':
    init_database()