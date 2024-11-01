# Employee Management Application
This is a simple Employee Management System built with **Django Rest Framework**. It allows users to add, edit, delete, and search employees after their successfull registration and login,
**Jwt** is used for token authentication,Django's built in database **Sqlite** is used.


## Features
* **Register**:Users can register in to application with their data.
* **Login**:Users can login in to application for handling their employees.
* **Add/Edit Employees**: Create or update employee details.
* **Delete Employees**: Delete employee details.


## Prerequisites
Make sure the following are installed on your machine

1.**Python**


## Installation and Usage

1. **clone the repository**

```
git clone https://github.com/your-username/employee-management.git
cd employee_management
```

2. **Create a .env in root directory**

```
SECRET_KEY=your_secret_key_here
DEBUG=True
```
3.**create a virtual environment**

```
python -m venv venv
source venv/bin/activate   # For Linux/macOS
venv\Scripts\activate      # For Windows
```

4.**Install dependencies**

```
pip install -r requirements.txt
```
5.**Apply migrations and run the server**

```
python manage.py migrate
python manage.py runserver
```
6.**Access the application**

```
http://127.0.0.1:8000
```

Enjoy building with the Employee Management System! 🚀





