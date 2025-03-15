# Reaction Bot Admin Panel

A modern Flask web application for managing reaction bots with authentication.

## Features

- Secure authentication system with admin login (username: admin, password: 1234)
- Modern and responsive UI with Bootstrap 5
- Bot management interface with add, edit, and delete functionality
- Database initialization with error handling
- Mobile-friendly design
- Toast notifications for user feedback
- Copy-to-clipboard functionality for bot tokens

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/reaction_bot_hook.git
cd reaction_bot_hook
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the required packages:
```bash
pip install -r requirement.txt
```

## Configuration

The application uses a default configuration with a hardcoded admin user:
- Username: `admin`
- Password: `1234`

You can modify the authentication settings in `scr/flask_app/models.py` to use a database or different credentials.

## Running the Application

Start the Flask development server:
```bash
python app.py
```

The application will be available at http://127.0.0.1:5000/

## Authentication

All routes in the application are protected by authentication. You need to log in with the admin credentials to access any page.

## Database Initialization

When you first run the application, you'll need to initialize the database. The application will show a message if the database is not initialized and provide a button to initialize it.

## Project Structure

- `app.py`: Main application entry point
- `scr/flask_app/`: Flask application package
  - `__init__.py`: Application factory and configuration
  - `models.py`: User model for authentication
  - `forms.py`: Form classes for the application
  - `routes/`: Application routes
  - `templates/`: HTML templates
  - `static/`: Static files (CSS, JS, images)
- `scr/database/`: Database handling code

## License

This project is licensed under the MIT License - see the LICENSE file for details. 