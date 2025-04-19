# Flask and Django Dockerized Applications

This project demonstrates two separate web applications, one built with Flask and the other with Django, orchestrated using Docker Compose.

## Project Structure
<details>
<summary>Click here to view project structure</summary>

```
.
├── docker-compose.yml
├── flask/
│   ├── app.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── templates/
│       ├── base.html
│       ├── index.html
│       ├── greet_form.html
│       └── greet_result.html
├── django/
│   ├── manage.py
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── myapp/             # Django project directory
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── wsgi.py
│   │   └── asgi.py
│   └── items/             # Django app directory
│       ├── __init__.py
│       ├── admin.py
│       ├── apps.py
│       ├── forms.py
│       ├── models.py
│       ├── tests.py
│       ├── views.py
│       ├── migrations/
│       └── templates/
│           └── home.html
└── README.md
```

</details>

## Flask Application (Port 5000)

A simple Flask application with the following features:

*   **Homepage (`/`)**: Displays a "Hello, World!" welcome message.
*   **Greeting Form (`/greet`)**:
    *   Presents a form to input a name and age.
    *   Accepts POST requests with the form data.
    *   Performs basic validation (checks if name is provided and age is numeric).
    *   Displays a greeting message (`Hello, [Name]! You are [Age] years old.`) upon successful submission.
    *   Shows an error message on the form if validation fails.

## Django Application (Port 8000)

A basic Django application for managing a list of items:

*   **Homepage (`/`)**:
    *   Displays a list of items retrieved from a SQLite database.
    *   Includes a form to add new items to the list.
*   **Admin Panel (`/admin/`)**:
    *   Provides the standard Django admin interface.
    *   Allows authenticated users (superuser) to Create, Read, Update, and Delete (CRUD) items. (Note: You'll need to create a superuser first).

## Running the Applications with Docker Compose

1.  **Prerequisites**: Make sure you have Docker and Docker Compose installed on your system.
2.  **Build and Run**: Navigate to the root directory containing the `docker-compose.yml` file and run:
    ```bash
    docker-compose up --build
    ```
    This command will build the Docker images for both the Flask and Django applications (if they don't exist) and start the containers.
3.  **Accessing the Apps**:
    *   **Flask App**: Open web browser and go to `http://localhost:5000`
    *   **Django App**: Open web browser and go to `http://localhost:8000`
4.  **Django Admin**:
    *   To access the Django admin panel at `http://localhost:8000/admin/`, we first need to create a superuser. Open another terminal, navigate to the project root, and run:
        ```bash
        docker-compose exec django-app python manage.py createsuperuser
        ```
    *   Follow the prompts to create your admin user.
    *   Now we can log in to the admin panel using the credentials you just created.
5.  **Stopping the Applications**: Press `Ctrl + C` in the terminal where `docker-compose up` is running. To remove the containers, run:
    ```bash
    docker-compose down
    ```
