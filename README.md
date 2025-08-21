#  Sports Quota Recruitment System

The Sports Quota Recruitment System is a web-based application designed to streamline the recruitment process for candidates applying under the sports quota. It enables candidates to register online with their personal, academic, and sports-related details while allowing administrators to manage applications efficiently.

Built using Django (Python Web Framework), this project ensures secure data handling, role-based access, and easy database management.

## Key Features

* __Candidate Registration__ – Candidates can apply online by filling in their personal, academic, and sports details.

* __Unique Registration Number__ – Every candidate receives a unique registration ID.

* __Document Upload__ – Candidates can upload required certificates and documents.

* __Admin Panel__ – Superusers can approve, reject, or update candidate applications.

* __Data Security__ – Validation checks for email, phone number, and date of birth.

* __Database Management__ – Candidate details stored securely using SQLite (default) or MySQL.

* __Simple UI__ – Easy-to-navigate web pages for candidates and administrators.

## 📂 Project Structure
```
Sports-Quota-Recruitment/
│── Sports_Qouta/            # Project configuration (settings, urls, wsgi, asgi)
│── registration/            # Django app for handling candidate registration
│── manage.py                # Django management script
```
## ⚙️ Prerequisites

Before setting up the project, make sure you have the following installed:

* Python (>= 3.8)

* Django (>= 4.0)

* pip (Python package manager)

* Virtualenv (recommended for dependency isolation)

* Database

  * SQLite (default, comes with Django)

  * OR MySQL (optional – configure in settings.py)

## 🚀 Installation & Setup

Follow these steps to set up the project locally:

__1. Clone the repository__
```
git clone https://github.com/deepshikha04yadav/Sports-Quota-Recruitment.git
cd Sports-Quota-Recruitment
```

__2. Create and activate a virtual environment (recommended)__
```
python -m venv venv
source venv/bin/activate     # For Linux/Mac
venv\Scripts\activate        # For Windows
```

__3. Install required dependencies__
```
pip install -r requirements.txt
```

__4. Apply database migrations__
```
python manage.py migrate
```

__5. Create a superuser for admin access__
```
python manage.py createsuperuser
```

__6. Run the development server__
```
python manage.py runserver
```

__7. Access the application in browser__

* Candidate Portal → http://127.0.0.1:8000/

* Admin Panel → http://127.0.0.1:8000/admin/

##  🔑 Admin Access

* Login with the credentials created using createsuperuser.

* Manage candidate registrations from the Django Admin Panel.

* Approve, reject, or update candidate applications.

## 🤝 Contribution Guidelines

Contributions are welcome! To contribute:

* Fork the repository.

* Create a new feature branch.

* Commit your changes.

* Push to your fork and open a pull request.
