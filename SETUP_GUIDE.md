# Global International College - Django Backend Setup Guide

## Project Structure
```
woods/
├── manage.py                    # Django management script
├── requirements.txt             # Python dependencies
├── db.sqlite3                   # Database (created after migrations)
├── school_site/                 # Project settings
│   ├── __init__.py
│   ├── settings.py             # Configuration
│   ├── urls.py                 # Main URL routing
│   └── wsgi.py                 # WSGI application
├── school/                      # Main Django app
│   ├── migrations/             # Database migrations
│   ├── models.py               # Data models
│   ├── views.py                # View functions
│   ├── urls.py                 # App URL routing
│   ├── forms.py                # Django forms
│   └── admin.py                # Admin configuration
├── templates/                   # HTML templates
│   ├── base.html               # Base template
│   └── school/                 # App templates
│       ├── index.html
│       ├── about.html
│       ├── academics.html
│       ├── admissions.html
│       ├── news.html
│       ├── news_detail.html
│       ├── contact.html
│       ├── login.html
│       ├── register.html
│       ├── portal.html
│       └── edit_profile.html
└── static/                      # Static files (CSS, JS, images)
    └── style.css               # CSS styling
```

## Installation & Setup

### 1. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 2. Apply Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

This will create the SQLite database with all necessary tables for:
- Users and Student Profiles
- News Articles
- Contact Messages
- Admission Applications
- Events

### 3. Create Admin User
```bash
python manage.py createsuperuser
```
Follow the prompts to create an admin account with email and password.

### 4. Run Development Server
```bash
python manage.py runserver
```

Visit: `http://localhost:8000/`

## Admin Access
- Admin URL: `http://localhost:8000/admin/`
- Login with your superuser credentials to:
  - Manage students and profiles
  - Create and publish news articles
  - View contact messages
  - Review admission applications
  - Create events

## Features Included

### ✅ User Management
- Student registration and login
- Student profiles with enrollment numbers
- Password authentication

### ✅ Contact System
- Contact form with email storage
- Admin dashboard to view all messages

### ✅ Admissions
- Online admission application form
- Document upload support
- Application status tracking
- Tuition information

### ✅ News Management
- Create, edit, and publish news articles
- Upload article images
- News display on homepage
- Individual article detail pages

### ✅ Student Portal
- Personalized student dashboard
- Profile management
- View enrolled information
- Quick action links

### ✅ Events
- Create and display upcoming events
- Event management in admin panel

## Default Admin Actions

1. **Add News Articles:**
   - Go to Admin → News → Add News
   - Write content and upload images
   - Check "Published" to make it visible

2. **Manage Students:**
   - View all enrolled students
   - Search by name or enrollment number
   - Update student information

3. **Review Contact Messages:**
   - View all submitted contact messages
   - Mark messages as read
   - Reply to enquiries

4. **Process Admissions:**
   - View all admission applications
   - Change status (pending/reviewed/approved/rejected)
   - Download submitted documents

## Database Reset (if needed)
```bash
# Delete database
rm db.sqlite3

# Recreate migrations
python manage.py makemigrations
python manage.py migrate

# Create new admin user
python manage.py createsuperuser
```

## Customization Tips

1. **Modify School Information:**
   - Update templates (templates/school/) with actual data
   - Edit footer information in base.html

2. **Add More Features:**
   - Edit models.py to add new data models
   - Create migrations: `python manage.py makemigrations`
   - Update views.py with new functionality
   - Add templates for new pages

3. **Styling:**
   - Edit base.html `<style>` section for global styles
   - Or create separate CSS files in `static/` folder

## Environment Variables (Production)
For production deployment, update settings.py:
```python
SECRET_KEY = 'your-secret-key'
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com']
```

## Email Configuration
Currently set to console email backend (prints to terminal). To use real email:
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
```

## Questions?
For Django documentation: https://docs.djangoproject.com/
For troubleshooting errors, check the terminal output when running the server.