# RiderApp

A RESTful API built with Django REST Framework that manages ride information including riders, drivers, and ride events.

## Tech Stack

- Python 3.14
- Django 5.x
- Django REST Framework
- SimpleJWT (Authentication)
- Django Filter
- SQLite (Development)

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/ferjohn-amistad/RiderApp.git
cd RiderApp
```

### 2. Create and Activate Virtual Environment
```bash
# Create virtual environment
python -m venv env

# Activate (Windows)
env\Scripts\activate


### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Migrations
```bash
python manage.py migrate
```

### 5. Create Superuser
```bash
python manage.py createsuperuser
```

### 6. Set Admin Role
```bash
python manage.py shell
```
```python
from rides.models import User
admin = User.objects.get(username='admin')
admin.role = 'admin'
admin.save()
```

### 7. Run the Server
```bash
python manage.py runserver
```

## Authentication

This API uses JWT authentication. Only users with the `admin` role can access the endpoints.

### Get Access Token
```
POST http://127.0.0.1:8000/api/token/
```
```json
{
    "username": "admin",
    "password": "yourpassword"
}
```

### Refresh Token
```
POST http://127.0.0.1:8000/api/token/refresh/
```
```json
{
    "refresh": "your_refresh_token",
    "access": "your_access_token"
}
```
## Include the access token in all API requests:

# API Endpoints

### Rides
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/rides/ | List all rides |
| POST | /api/rides/ | Create a ride |
| GET | /api/rides/{id}/ | Get a ride |
| PUT | /api/rides/{id}/ | Update a ride |
| DELETE | /api/rides/{id}/ | Delete a ride |

### Users
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/users/ | List all users |
| POST | /api/users/ | Create a user |
| GET | /api/users/{id}/ | Get a user |
| PUT | /api/users/{id}/ | Update a user |
| DELETE | /api/users/{id}/ | Delete a user |


## Filtering

### Filter by status
GET /api/rides/?status=en-route

### Filter by rider email
GET /api/rides/?rider_email=rider@email.com



## Sorting

### Sort by pickup time
GET /api/rides/?ordering=pickup_time

### Sort by distance to a GPS location
GET /api/rides/?lat=10.3157&lng=123.8854

## Pagination
GET /api/rides/?page=2

## EVALUATION

### Functionality: Does the application meet every requirement above?
I believe all the requirements have been met:
- Models are defined with fields you've provided.
- ViewSets can hadle full CRUD operations
- Seriealizers are implemented
- API access has been restricted to users with admin role
- Can support pagination
- Filtering by `status` and `rider_email` is supported
- Distance can be sorted from a given GPS location
- 'todays_ride_events' can return RideEvents from the last 24hrs

### Code Quality: Is the code modular, readable, and maintainable?
Codes is seperated into different modules, very readable and can easily maintained


### Error Handling: Are errors and edge cases handled properly?
I have added several error handlers for unauthenticared request, non-admin users and for invalid lat/lng query paramaters

### Performance: Is the API tuned to make as few SQL queries as possible?
- Ride List API runs in 2-3 total SQL queries
- Database indexes added on `status`, `pickup_time`, and `created_at` for faster filtering and sorting
- `select_related` is used to fetch rider and driver in a single SQL query


### Challenges
The most challenging for me is researching and finding similar codes for getting the logic of the 'get_queryset' function.


## Bonus SQL Query

```sql
SELECT
    strftime('%Y-%m', pickup.created_at) AS month,
    u.first_name || ' ' || u.last_name AS driver_name,
    COUNT(*) AS trip_count
FROM rides_ride r
JOIN rides_rideevent pickup ON pickup.id_ride_id = r.id_ride
    AND pickup.description = 'pickup'
JOIN rides_rideevent dropoff ON dropoff.id_ride_id = r.id_ride
    AND dropoff.description = 'dropoff'
JOIN rides_user u ON u.id_user = r.id_driver_id
WHERE (
    strftime('%s', dropoff.created_at) - strftime('%s', pickup.created_at)
) > 3600
GROUP BY month, u.id_user
ORDER BY month, driver_name;
```

### Expected Output
| month | driver_name | trip_count |
|-------|-------------|------------|
| 2024-01 | Maria S. | 3 |
| 2024-01 | John D. | 5 |
| 2024-02 | Maria S. | 2 |