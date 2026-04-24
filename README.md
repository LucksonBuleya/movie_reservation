# Movie Reservation System (Backend)

A Django REST API for booking movie tickets, managing showtimes, and handling seat reservations.

## Features
- User authentication
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
```

## Request Architecture Flow

| Step | Description | Example |
|------|-------------|---------|
| HTTP Request | Client sends request to API | `POST /api/bookings/bookings/` |
| URL Router (`urls.py`) | Matches endpoint to correct view | Routes request to `BookingViewSet` |
| View Class | Handles request logic | Creates booking request |
| Serializer | Validates and formats data | Checks `showtime`, seats, price |
| Model | Interacts with database | Saves booking record |
| HTTP Response | Returns JSON result | `201 Created` + booking data |

## Quick API Test (cURL)

### Register User
```bash
curl -X POST http://127.0.0.1:8000/api/users/register/ \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"john\",\"email\":\"john@example.com\",\"password\":\"testpass123\"}"
```

### Get JWT Token
```bash
curl -X POST http://127.0.0.1:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"john\",\"password\":\"testpass123\"}"
```

### List Movies
```bash
curl http://127.0.0.1:8000/api/movies/movies/
```

### Create Booking (Protected Route)
```bash
curl -X POST http://127.0.0.1:8000/api/bookings/bookings/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"showtime\":1,\"total_price\":\"100.00\"}"
```

### View Available Seats
```bash
curl http://127.0.0.1:8000/api/movies/showtimes/1/available_seats/
```
