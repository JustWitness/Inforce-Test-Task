# Inforce-Test-Task
A Django-based REST API for managing restaurant menus and employee voting. Built with **Django REST Framework** and secured with **JWT Authentication**.

## Features
* **Role-Based Access Control**: Separate permissions for Restaurants and Employees.
* **Menu Management**: Restaurants can upload and manage daily menus.
* **Voting System**: Employees can view available menus and cast one vote for their favorite.
* **Daily Reset**: Logic built around `timezone.localdate()` to ensure menus and voting results are fresh every day.
* **Automated Testing**: Full coverage for registration, login, logout, and menu operations.
* **Code Quality**: Project adheres to PEP 8 standards using **Flake8**.

## Tech Stack
* **Framework**: Django & Django REST Framework
* **Auth**: SimpleJWT
* **Database**: PostgreSQL
* **Linter**: Flake8

---

## Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/JustWitness/Inforce-Test-Task.git
cd Inforce-Test-Task
```

### 2. Run with Docker

Ensure you have Docker and Docker Compose installed:
```bash
docker-compose up --build
```

The API will be available at: **[http://localhost:8000](http://localhost:8000)**

Database Details:
* **Type:** PostgreSQL
* **Host:** `localhost`
* **Port:** `5432`
* **Username/Password** `postgres`/`postgres`

---

## Testing & Quality

### Run Unit Tests
```bash
docker-compose exec web python manage.py test 
```
### Run Linter
```bash
docker-compose exec web flake8
```

---

## API Reference

### Authentication

* **POST** `/api/register/` – Register as a Restaurant or Employee  
* **POST** `/api/login/` – Login to receive Access and Refresh tokens  
* **POST** `/api/logout/` – Blacklist the Refresh token  

---

### Menu Operations

* **POST** `/api/menu/` – (Restaurant only) Create today's menu  
* **GET** `/api/available/` – (Employee only) List all menus for the current day  
* **POST** `/api/vote/` – (Employee only) Cast a vote for a specific menu  
* **GET** `/api/results/` – (Employee only) View the winning menu of the day  

---

## Admin Access

Create a superuser:
```bash
docker-compose exec web python manage.py createsuperuser
```

Use the email address you provided during the superuser creation to log into the [Admin Panel](http://localhost:8000/admin/)
