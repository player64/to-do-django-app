# Todo App

This is a simple task management (Todo) application developed using Django and Django REST Framework. The application allows users to manage their tasks. Each user can create tasks, view their own tasks, edit, update status and delete them. The tasks are ordered by status and creation date (latest first).

## Main Features

- User registration and authentication.
- JWT Token based authentication.
- CRUD operations for tasks.
- Task viewable per user.
- Each task contains: title, description, date of creation, status (to-do, doing, done) and date of last update.
- Task status enumeration (to-do, doing, done).
- Task ordering by status and creation date.

## Requirements

- Python 3.9+
- Django 4.2.1+
- Django Rest Framework 3.14+
- Django Rest Framework Simple JWT 5.2.2+

## Installation & Setup

1. Clone the repository:
   ```
   git clone https://github.com/player64/to-do-django-app.git
   ```
2. Enter the project directory:
   ```
   cd to-do-django-app
   ```
3. Create and activate a virtual environment:
   ```
   python3 -m venv venv
   source venv/bin/activate
   ```
4. Install requirements:
   ```
   pip install -r requirements.txt
   ```
5. Apply migrations:
   ```
   python manage.py migrate
   ```
6. Run the server:
   ```
   python manage.py runserver
   ```
Now, you can browse the API at `http://127.0.0.1:8000`.

## Running Tests

To run the tests, use the following command in the terminal:

```
python manage.py test
```

This will run all the test cases written for the app.

## API Endpoints

The application provides the following endpoints:

1. User registration: `/api/v1/user/register/`
2. User login: `/api/v1/user/login/`
3. User logout: `api/v1/user/logout`
4. User token refresh: `/api/v1/token/refresh/`
5. List/Create tasks: `/api/v1/task/`
6. Retrieve/Update/Delete task: `/api/v1/task/<id>/`

## Future Enhancements

1. Add ability to share tasks with other users.
2. Add the user interface using a frontend framework like React or Vue.
3. Expand the task attributes (e.g., adding tags or priority level).
4. Implementation of dynamic order by status, date etc.
5. Search tasks by keyword
6. Reset user password
7. Implement email notifications for task deadlines.


