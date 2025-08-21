#  Sports Quota Recruitment System

The Sports Quota Recruitment System is a web-based application designed to streamline the recruitment process for candidates applying under the sports quota. It enables candidates to register online with their personal, academic, and sports-related details while allowing administrators to manage applications efficiently.

Built using Django (Python Web Framework), this project ensures secure data handling, role-based access, and easy database management.

---

## 🌟 Features

- **Candidate Registration:** Simple multi-step form collects personal, academic, and sports details.
- **Unique Registration Number:** Auto-generated for every candidate for easy tracking.
- **OTP Verification:** Mobile number verification ensures authentic registration.
- **Document Uploads:** Candidates upload supporting certificates and documents (PDF, Doc, etc.).
- **Captcha Security:** CAPTCHA is integrated to prevent spam submissions.
- **Status Tracking:** Candidates can check their application status at any time using registration number and captcha.
- **Admin Dashboard:** Superusers can review applications, approve/reject candidates, and view individual profiles.
- **Email Notification:** Automatic email is sent to candidates when application status changes.
- **Search & Filter:** Admins can quickly search applications by registration number.
- **Logout & Session Security:** Secure session management with logout functionality for admins.
- **Responsive UI:** Modern, mobile-friendly interface with clear navigation.
- **Configurable Database:** Works out-of-the-box with SQLite, or switch to MySQL for production.

---

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

## Output
<img width="1919" height="878" alt="Screenshot 2025-08-19 103148" src="https://github.com/user-attachments/assets/733a7fe0-9eda-4b08-b958-f21f8a868972" />
<img width="1896" height="870" alt="Screenshot 2025-08-19 103236" src="https://github.com/user-attachments/assets/d3a67904-8d4b-4a7b-b5c4-cb5879167518" />
<img width="1919" height="873" alt="Screenshot 2025-08-19 103459" src="https://github.com/user-attachments/assets/6e38d9d2-436f-4b3a-9cfa-0f4c61ef8798" />



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
