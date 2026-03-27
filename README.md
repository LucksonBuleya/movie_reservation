# Movie Reservation System (Backend)

A Django REST API for booking movie tickets, managing showtimes, and handling seat reservations.

## Features
- User authentication (JWT - coming next)
- Movie listing and details
- Theater and seat management
- Showtime scheduling
- Ticket booking system (in progress)

## Tech Stack
- Django
- Django REST Framework
- PostgreSQL (planned)

## Setup

```bash
git clone https://github.com/yourusername/movie-reservation.git
cd movie-reservation
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver