Flask Ticket System
===================

Overview
--------

Flask Ticket System is a web application for managing tickets with different user roles and groups. The application is built using Flask, SQLAlchemy, and Flask-Login.

Features
--------

- User registration and authentication
- Role-based access control (Admin, Manager, Analyst)
- Ticket management with different statuses (Pending, In review, Closed)
- Group assignment for tickets
- Admin can create, assign groups, and delete any ticket
- Manager can update the status of tickets assigned to their group
- Analyst can update the description of tickets assigned to their group

Setup
-----

To set up the Flask Ticket System, follow these steps:


1. Create and activate a virtual environment:

    On macOS and Linux:

    python -m venv venv

    source venv/bin/activate

    On Windows:

    python -m venv venv

    `venv\Scripts\activate`

2. Install the dependencies:

    pip install -r requirements.txt

3. Set up the database:

    flask db init,

    flask db migrate -m "Initial migration",

    flask db upgrade

4. Initialize roles, groups, and users:

    python init_db.py

5. Run the application:

    flask run

Usage
-----

- Navigate to `http://127.0.0.1:5000` in your web browser.
- Register a new user and select the desired role and group.
- Log in with the registered user credentials.
- Admin can create, assign groups, and delete tickets.
- Manager can update the status of tickets assigned to their group.
- Analyst can update the description of tickets assigned to their group.