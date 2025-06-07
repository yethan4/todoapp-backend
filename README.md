# To-Do App

> The backend is hosted on Render, so it may take up to a minute to start after the first request. Thank you for your patience!

- **Live app:** [todoapp-yethan.netlify.app](https://todoapp-yethan.netlify.app/login)  
- **Backend API:** [backend-api](https://todoapp-backend-7b8u.onrender.com/)
- **Frontend repository** [https://github.com/yethan4/todoapp-frontend](https://github.com/yethan4/todoapp-frontend)

## About This Project

This is a simple To-Do application with a React frontend and a Django REST Framework backend.  
**This project was created quickly as my first attempt at building a full-stack app in Django + React.**  
It is not perfect, but it helped me learn the basics of building and connecting these technologies together.

---

## Technologies Used

- **Frontend**: React, TypeScript, React Context API, Axios - see [frontend](https://github.com/yethan4/todoapp-frontend)
- **Backend**: Python (Django REST Framework, JWT authentication)

---

## Description

This project is a simple To-Do application with a Django REST Framework backend and a React frontend. The backend provides a RESTful API for managing tasks and lists, as well as JWT-based user authentication.

---

## Purpose
This is a very simple and basic application, created primarily to demonstrate my understanding of:

* Building a basic backend with Django REST Framework
* Implementing JWT-based authentication
* Connecting a React frontend with an API backend

---

# API Endpoints

**All endpoints below are prefixed with `/api/`, e.g. `/api/register/`**  
**All endpoints (except registration and login) require JWT authentication.**  
Send the token in the `Authorization: Bearer <token>` header.

## Authentication & User

- **POST `/register/`**  
  Register a new user.  
  **Body:**  
  ```json
  {
    "username": "user",
    "email": "mail@example.com",
    "password1": "password"
    "password2": "password"
  }
  ```
  Returns user data and JWT tokens.

- **POST `/login/`**  
  Obtain JWT tokens (login).  
  **Body:**  
  ```json
  {
    "email": "mail@example.com",
    "password": "password",
  }
  ```
  Returns `refresh` and `access` tokens.

- **POST `/logout/`**  
  Logout (invalidate refresh token).  
  **Body:**  
  ```json
  {
    "refresh": "..."
  }
  ```

- **POST `/token/refresh/`**  
  Refresh JWT access token.  
  **Body:**  
  ```json
  {
    "refresh": "..."
  }
  ```
  Returns new `access` token.

- **GET `/user/`**  
  Get information about the currently authenticated user.



## Tasks

- **GET `/tasks/`**  
  List your tasks for today (filter by `date` and `task_list` query params).

  - Tasks due on a specific date:
  ```
  GET /api/tasks/?date=2025-06-15
  ```
  - Tasks in a specific list:
  ```
  GET /api/tasks/?task_list=2
  ```

  **Example response:**
    ```json
    [
      {
        "pk": 1,
        "title": "Buy milk",
        "due_date": "2025-06-07",
        "completed": false,
        "task_list": null
      },
      {
        "pk": 2,
        "title": "Study Django",
        "due_date": "2025-06-07",
        "completed": true,
        "task_list": null
      }
    ]
    ```

- **POST `/tasks/`**  
  Creates a new task.  
  **Request body:**
  ```json
  {
    "title": "Task title",
    "due_date": "YYYY-MM-DD",       
    "task_list": null          
  }
  ```


- **PATCH `/tasks/<pk>/set-completed/`**  
  Set the completion status of a task.  
  **Body:**  
  ```json
  {
    "completed": true
  }
  ```

- **PATCH `/tasks/<pk>/update/`**  
  Edit an existing task.  
  **Body:**  
  Any fields to update, e.g.:
  ```json
  {
    "title": "New title",
    "due_date": "YYYY-MM-DD",
    "task_list": 2 
  }
  ```

- **DELETE `/tasks/<pk>/delete/`**  
  Delete a task.


## Lists

- **GET `/lists/`**  
  List all your lists.

- **POST `/lists/`**  
  Create a new list.  
  **Body:**  
  ```json
  {
  "name": "New List",
  "slug": "new-list"
  }
  ```

- **GET `/lists/<slug>/`**  
  Get details of a list.

- **DELETE `/lists/<slug>/`**  
  Delete a list.

---

## Notes

- All operations on tasks and lists are scoped to the authenticated user.
- The task list endpoint returns tasks for today by default (unless you use filters).

---

# Local Installation

## Backend Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yethan4/todoapp-backend
   cd todoapp-backend
   ```

2. **Create and activate a virtual environment**

   On macOS/Linux:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
   On Windows:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **(Optional) Configure environment variables**  
   Create a `.env` file and set at least:
   ```
   SECRET_KEY=your_secret_key
   DEBUG=True
   ALLOWED_HOSTS=127.0.0.1 localhost
   ```
   If you use CORS, add:
   ```
   CORS_ALLOWED_ORIGINS=http://localhost:3000
   ```
   If you want to use a custom database (e.g. PostgreSQL), set:
   ```
   DATABASE_URL=postgres://USER:PASSWORD@HOST:PORT/DBNAME
   ```
   If `DATABASE_URL` is not set, the app will use the default SQLite database.

5. **Apply database migrations**
   ```bash
   python manage.py migrate
   ```

6. **(Optional) Create a superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the server**
   ```bash
   python manage.py runserver
   ```

The API will be available at `http://127.0.0.1:8000/`.

---

## Frontend Setup

See instructions in the [frontend repository](https://github.com/yethan4/todoapp-frontend).

---

## Troubleshooting

- If you use the frontend and backend separately, make sure to configure CORS (`django-cors-headers`) in your backend settings.
- If you encounter issues, ensure all dependencies are installed and that your environment variables are set.
