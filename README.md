# random-adventure-generator
The Random Adventure Generator is a fun and interactive bot that provides users with random challenges or "adventures" to complete in various categories. The bot offers a personalized experience, tracks progress. It serves as a motivational tool to encourage users to try new activities.

## Technologies
1. **Python** - The main programming language used for the project.
2. **Flask** - A lightweight web framework for building APIs.
3. **SQLAlchemy** - An ORM used to interact with the database.
4. **SQLite** - A robust relational database for storing user and adventure data.
5. **Gunicorn** - A Python WSGI HTTP server used for deployment.
6. **Render** - A cloud platform for deploying the application.
7. **Flasgger (Swagger)** - Provides automatic API documentation and testing.
8. **Flask-Limiter** - Adds rate-limiting capabilities to the app, with Redis as the storage backend.
9. **Redis** - An in-memory data store used with Flask-Limiter for rate-limiting.
10. **OpenAI** - Integrates GPT-based functionality for generating adventure content.

## Getting Started

Follow the steps below to set up and run the project locally:

1. **Clone the repository:**

    ```bash
    git clone https://github.com/DenisGavar/random-adventure-generator.git
    cd random-adventure-generator
    ```
2. **Set up a virtual environment:**

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Copy .env file:**

    ```bash
    cp .env.example .env
    ```

    Fill in the required values in `.env`.

4. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

5. **Run migrations:**

    This project uses Flask-Migrate for database migrations.

    Initialize migrations:
    ```bash
    FLASK_APP="run:create_app('development')" flask db init
    ```

    Generate a new migration script:
    ```bash
    FLASK_APP="run:create_app('development')" flask db migrate -m "Initial migration"
    ```

    Apply the migration to the database:
    ```bash
    FLASK_APP="run:create_app('development')" flask db upgrade
    ```

6. **Start app:**

    ```bash
    python run.py
    ```