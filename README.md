# Library-Management-System-Django-CRUD-App-
A web-based Library Management System built using Django that allows librarians to manage books, members, and borrow/return transactions efficiently.

## Features
- Add, edit, delete books, authors, categories, and members
- Record book borrow and return transactions
- Track overdue books and highlight overdue borrowers
- Search books by title, author, or category
- User authentication for librarians
- Session-based theme (light/dark)

## Technologies Used
- Python 3.11.9
- Django 5.2.8
- HTML, CSS (with custom themes)
- SQLite3 (default database)

## Installation
1. Clone the repository: [GitHub Repository](https://github.com/Liyamol06/Library-Management-System-Django-CRUD-App-.git)
2. Navigate to the project folder:
  ```
   cd Library-Management-System-Django-CRUD-App-
  ```
3. Create a virtual environment: 
  ```
  python -m venv venv 
  ```
4. Activate the virtual env
- Windows:
  ```
  venv\Scripts\activate
  ```
- macOS/Linux:
  ```
  source venv/bin/activate
  ```
5. Install dependencies: 
  ```
  pip install -r requirements.txt
  ```
7. Navigate to project:  
  ```
  cd library_management
  ```
7. Apply migrations: 
  ```
  python manage.py migrate
  ```
8. Create a superuser (librarian):  
  ```
  python manage.py createsuperuser
  ```
9. Run the development server:  
  ```
  python manage.py runserver
  ```
10. Open in browser:  http://127.0.0.1:8000/

## Usage
- Log in with your librarian credentials.
- Navigate the dashboard to manage books, authors, categories, and members.
- Borrow and return books using the Borrower module.
- Overdue books are highlighted on the dashboard and borrower list(red color).
