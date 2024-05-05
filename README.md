Peagsus: Flight Management System

Features

* Database Schema: Detailed schema including tables for Flights, Airline_Companies, Users, Countries, Tickets, Customers, User_Roles, and Administrators.
* Data Integrity: Use of primary keys (PK), foreign keys (FK), auto-increment (AI), and unique (U) constraints to ensure data integrity.
* Flight Management: Capabilities to add, update, and query flight information, including departure and landing times, and manage remaining tickets.
* Airline and Customer Management: Manage airline companies and customer information, including sensitive data such as credit card numbers securely.
* User Roles and Authentication: Differentiated access and operations based on user roles, ensuring system security and integrity.
* Comprehensive Ticketing System: Ticket management functionality, linking flights to customers and handling transactions.

Usage

The system is designed for use by airlines, travel agencies or private travelers, and administrative users with varying levels of access.

Tech Stack

* Database: SQL Server is employed for its robust data management capabilities, handling the storage, retrieval, and manipulation of relational data with high performance and reliability.
* Backend: The Flask Rest Framework is used to create a powerful API layer. It facilitates the development of RESTful APIs, allowing for flexible, efficient, and scalable backend services.
* Frontend: A Flask-based user interface provides a straightforward and effective way for users to interact with the system. While Flask is traditionally seen as a backend framework, it can also serve HTML templates, enabling the creation of dynamic web pages for managing and displaying flight information, user accounts, and more.

Screenshots

Homepage 
![Homepage](/screenshots/pegasus1.jpg "Homepage")

Flights
![Flights](/screenshots/pegasus2.jpg "Flights")

Manage Customers
![ManageCustomers](/screenshots/pegasus3.jpg "Manage Customers")

This project was developed as part of Python Full Stack Development course, at John Bryce College.