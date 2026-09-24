# Habit Tracker

A Flask + PostgreSQL REST API for tracking daily/weekly habits, with full user authentication and per-user data ownership. Built as part of a backend development internship to practice real-world CRUD, auth, and database integrity patterns.

## Features

- **User authentication** — registration and login with hashed passwords (Werkzeug's `generate_password_hash` / `check_password_hash`), session-based auth via signed cookies
- **Full CRUD** on habits — create, read, update, and delete
- **Per-user data ownership** — habits are linked to the user who created them via a foreign key (`userid` referencing `users(id)`); users can only view, edit, or delete their own habits, enforced both in queries and at the database level
- **Route protection** — all data routes require a valid logged-in session
- **HTML forms** — register and add habits via server-rendered forms, in addition to a JSON API
- **Error handling** — clean status codes throughout: `400` for missing fields, `401` for unauthenticated requests, `404` for not-found or not-owned resources, `504` for database connection failures
- **Automated tests** — a `pytest` suite using Flask's `test_client()` covering authentication and access control

## Tech stack

- **Flask** — web framework
- **PostgreSQL** (hosted on [Neon](https://neon.tech)) — database
- **psycopg2** — Postgres driver
- **Werkzeug security** — password hashing
- **python-dotenv** — environment variable management
- **pytest** — automated testing

## Setup

1. Clone the repo and install dependencies:
   ```bash
   pip install flask psycopg2-binary python-dotenv pytest requests
   ```

2. Create a `.env` file in the project root with:
   ```
   DATABASE_URL=your_postgres_connection_string
   SECRET_KEY=your_secret_key
   ```

3. Run the database setup scripts (create the `users` and `habittracker` tables, then link them with the `userid` foreign key).

4. Start the app:
   ```bash
   python app.py
   ```

5. Run the test suite:
   ```bash
   pytest
   ```

## API Overview

| Method | Route | Description | Auth required |
|---|---|---|---|
| POST | `/register` | Register a new user (JSON) | No |
| GET | `/register-form` | Show HTML registration form | No |
| POST | `/submit-register-form` | Register via HTML form | No |
| POST | `/login` | Log in (JSON) | No |
| GET | `/login-form` | Show HTML login form | No |
| POST | `/submit-login-form` | Log in via HTML form | No |
| GET | `/` | List your habits | Yes |
| POST | `/add-habit` | Add a new habit (JSON) | Yes |
| GET | `/add-habit-form` | Show HTML add-habit form | No |
| POST | `/submit-habit` | Add a habit via HTML form | Yes |
| PUT | `/update-habit/<id>` | Update one of your habits | Yes |
| DELETE | `/delete/<id>` | Delete one of your habits | Yes |

## What this project demonstrates

This project was built incrementally to practice:
- Parameterized SQL queries (preventing SQL injection)
- Password hashing and salted comparison
- Session-based authentication with signed cookies
- Relational data integrity via foreign keys
- Defensive query design (`WHERE id = %s AND userid = %s`) to enforce ownership even against guessed IDs
- Structured error handling with correct HTTP status codes
- Writing automated tests to replace manual API testing
