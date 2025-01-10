# Library Management System API

This project is a Library Management System API built with Django and Django REST Framework (DRF). It allows users to manage books, perform CRUD operations on books and users, and handle borrowing and returning books. The API is designed to be secure, scalable, and RESTful.

## Features

### **Books Management**
- Create, Read, Update, and Delete (CRUD) books.
- Each book has the following attributes:
  - Title
  - Author
  - ISBN (unique)
  - Published Date
  - Number of Copies Available
- Search for books by title, author, or ISBN.

### **Users Management**
- Create, Read, Update, and Delete (CRUD) users.
- Each user has:
  - Username (unique)
  - Email
  - Date of Membership
  - Active Status

### **Book Borrowing**
- Users can borrow a book if copies are available.
- Users can only borrow one copy of a specific book at a time.
- Tracks checkout and return dates.

### **Book Returning**
- Users can return borrowed books.
- Increases the number of available copies upon return.

### **Authentication**
- Basic authentication for API access.
- Users can log in and view their borrowing history.
- Supports token-based authentication for enhanced security.

### **Deployment**
- Hosted on PythonAnywhere for easy accessibility.
- Accessible at: `<Your Deployed URL>` (replace with your deployment URL)

---

## Installation and Setup

### **Prerequisites**
- Python 3.8+
- Django 5.0+
- Django REST Framework
- A virtual environment manager (e.g., `venv` or `pipenv`)

### **Local Setup**
1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd LibraryManagementSystemAPI