#  SmartPark – Vehicle Parking App

A full-stack, multi-user **4-wheeler parking management system** built using Flask and VueJS.  
The application efficiently manages parking lots, parking spots, and vehicle reservations with role-based access for **Admin** and **User**.

---

##  Project Overview

**Project Title:** Vehicle Parking App – V2  
**Developed By:** Vishnu Kumar Jha  
**Program:** BS in Data Science, IIT Madras  

This application is designed to automate parking operations such as spot allocation, cost calculation, reminders, and reporting using a scalable backend and a modern frontend.

---

## Problem Statement

Managing parking lots manually is inefficient and error-prone. This system provides a centralized platform to:

- Manage multiple parking lots and spots
- Allow users to book, occupy, and release parking spots
- Automate cost calculation and reporting
- Improve operational efficiency using caching and background jobs

---

##  System Roles

###  Admin
- Create, edit, and delete parking lots
- Automatically generate parking spots based on lot capacity
- View parking usage statistics and summaries
- Monitor overall system activity

###  User
- Register and log in securely
- Book available parking spots
- Occupy and release parking spots
- View parking history and cost details
- Export parking history as CSV

---

##  Technologies Used

### Backend
- **Flask** – REST API framework
- **SQLAlchemy** – ORM for database modeling
- **Flask-JWT-Extended** – JWT-based authentication
- **Celery** – Asynchronous background jobs
- **Redis** – Caching and Celery message broker
- **Flask-Mail** – Automated email notifications

### Frontend
- **VueJS** – Interactive user interface
- **Bootstrap 5** – Responsive UI design
- **Chart.js** – Dashboard analytics and charts

### Database
- **SQLite** – Programmatically created relational database

---

##  Database Design

The system uses the following core entities:

- **User** – Stores admin and user accounts with authentication details
- **ParkingLot** – Stores parking lot details such as name, address, price, and capacity
- **ParkingSpot** – Represents individual parking spots and their status
- **Reservation** – Tracks parking reservations, timestamps, and cost

/exports/           # Generated CSV exports
/instance/          # SQLite database
