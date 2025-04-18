# 8EDZ9-24126
Pars Tasmim Code Challenge

# Table Booking API

A simple restaurant reservation system built with Django REST Framework.

## Features

- User-authenticated table bookings
- Pricing logic based on seat count
- PostgreSQL-backed storage
- OpenAPI schema via drf-spectacular
- Dockerized for easy development

## Getting Started

### Requirements

- Docker
- Docker Compose

### Run the project

```bash
docker-compose up --build
```
App will be available at: http://localhost:8000

### API Endpoints
- POST /book/ – Create a booking

`GET /book/` – List user's bookings

`GET /book/<id>/` – Retrieve a booking

`DELETE /cancel/<id>/` – Cancel a booking

### Running Tests
```bash
docker-compose run web python manage.py test
```