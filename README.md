# IST-Smart-Hostel

IST-Smart-Hostel is a web-based application designed to streamline hostel management processes. It offers functionalities such as student registration, room allocation, and administrative controls to enhance efficiency and user experience.

## Features

* **Student Registration**: Allows students to register and manage their profiles.
* **Room Allocation**: Facilitates the assignment of rooms to students based on availability.
* **Administrative Dashboard**: Provides administrators with tools to manage students, rooms, and other hostel-related activities.
* **User Authentication**: Ensures secure access for both students and administrators.

## Technologies Used

* **Frontend**: HTML, CSS (located in the `static/` directory)
* **Backend**: Python with Flask framework
* **Database**: SQLite (managed via SQLAlchemy ORM)

## Project Structure

```
IST-Smart-Hostel/
├── app.py             # Main application file
├── forms.py           # Defines Flask-WTF forms
├── init_db.py         # Initializes the database
├── models.py          # Database models
├── routes.py          # Application routes
├── utils.py           # Utility functions
├── requirements.txt   # Python dependencies
├── static/            # Static files (CSS, JS, images)
├── templates/         # HTML templates
└── README.md          # Project documentation
```



## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/abdullahhasif/IST-Smart-Hostel.git
   cd IST-Smart-Hostel
   ```



2. **Create a virtual environment**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```



3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```



4. **Initialize the database**:

   ```bash
   python init_db.py
   ```



5. **Run the application**:

   ```bash
   python app.py
   ```



Access the application at `http://localhost:5000`.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
