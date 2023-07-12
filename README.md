# To-Do List Web Application

A simple To-Do Flask web application that allows users to create, manage, and organize their tasks. The application provides features such as user authentication, creating to-do items with title, description, and time, and the ability to upload images (available with a Pro license).

## Features

- User authentication with Keycloak
- GraphQL API for handling to-do operations
- List all to-do items
- Add a new to-do item
- Delete an existing to-do item
- Edit an existing to-do item
- Pro license for image uploads (via Stripe payment integration)
- Clean and user-friendly UI (built with React)

## Installation

1. Clone the repository:

```shell
git clone https://github.com/your-username/todo-list.git
```
```cd todo-list```

```pip install -r requirements.txt```

```python manage.py runserver```

# Acknowledgements
Keycloak - Open-source identity and access management for modern applications.

Flask - Python web framework used for building the backend.

GraphQL - Query language for APIs.

Stripe - Online payment processing platform.

React - JavaScript library for building user interfaces.
