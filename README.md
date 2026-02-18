# Visitor Management System

A Django-based web application to manage visitor registration, entry/exit tracking, employee attendance, and basic reporting for organizations and hostels.

## Key Features
- Visitor registration with photo and digital signature
- Check-in / check-out tracking
- Employee attendance management
- Admin dashboard with reports
- Email notifications
- CSV report export

## Tech Stack
- Backend: Python, Django
- Frontend: HTML, CSS, JavaScript
- Database: SQLite3
- Tools: Git, GitHub

## Project Highlights
- Built using Django MVC architecture
- Database-driven application with relational models
- Secure authentication and role-based access
- Real-world use case implementation

## Setup (Quick Start)
```bash
git clone https://github.com/sakshi6301/Visitor_Management.git
cd Visitor_Management
python -m venv venv
venv\Scripts\activate
pip install django
python manage.py migrate
python manage.py runserver
