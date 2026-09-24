# Student Support & Ticket Management System

A Django-based Student Support and Ticket Management System designed to help students raise support requests and allow staff to manage, prioritize, assign, and resolve those requests.

## Features

### Student
- Login
- Create support tickets
- Select ticket category
- Set ticket priority
- View own tickets
- View ticket details
- Add comments
- View activity history

### Staff
- Login
- View all student tickets
- Update ticket status
- Change ticket priority
- Assign tickets to staff members
- View ticket age
- View SLA status
- Track overdue tickets
- Activity history for ticket changes

### Manager
- Login
- View overall ticket statistics
- View overdue tickets
- View high-priority tickets
- View staff workload
- Monitor ticket status distribution

## Ticket Categories

- Fees
- Attendance
- ID Card
- Documents
- Certificates
- Other

## Ticket Status

- Open
- In Progress
- Pending
- Resolved
- Closed

## Priority Levels

- Low
- Medium
- High

## SLA

The prototype uses priority-based calendar-day SLAs:

- High Priority: 1 day
- Medium Priority: 2 days
- Low Priority: 3 days

## Technology Stack

- Python
- Django
- SQLite
- HTML
- CSS
- Django Authentication
- Django Groups for role management

## User Roles

The application uses Django Groups for role-based access:

- Student
- Staff
- Manager

Each role has access only to the functionality relevant to that role.

## Project Structure

```text
student_support/
│
├── manage.py
│
├── student_support/
│   ├── settings.py
│   ├── urls.py
│   └── ...
│
└── tickets/
    ├── models.py
    ├── views.py
    ├── forms.py
    ├── urls.py
    ├── admin.py
    ├── management/
    ├── migrations/
    ├── templates/
    └── static/