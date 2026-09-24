# Student Support & Ticket Management
## Approach, Assumptions, Architecture and Trade-offs

## 1. Approach

The system is designed as a role-based student support and ticket management platform.

Students can:
- Create support tickets
- Select a category and priority
- View their own tickets
- View ticket details and activity history
- Add comments to their tickets

Staff can:
- View all tickets
- Update ticket priority and status
- Assign tickets to staff members
- Monitor ticket age and SLA status
- Add updates through ticket activities

Managers can:
- View overall ticket statistics
- Monitor open, pending, resolved and closed tickets
- View high-priority and overdue tickets
- View staff workload based on assigned tickets

The system also maintains ticket activity history whenever important ticket properties are changed.

---

## 2. Assumptions

The following assumptions were made while implementing the system:

1. A student can create tickets only for themselves.
2. Staff members are responsible for processing and updating tickets.
3. Managers require an overview of ticket activity rather than directly processing tickets.
4. Each ticket has one student as its creator.
5. A ticket can optionally be assigned to one staff member.
6. Tickets can have the following categories:
   - Fees
   - Attendance
   - ID Card
   - Documents
   - Certificates
   - Other
7. Tickets can have Low, Medium or High priority.
8. Tickets can have Open, In Progress, Pending, Resolved or Closed status.
9. SLA due dates are calculated according to priority:
   - High: 1 day
   - Medium: 2 days
   - Low: 3 days
10. A ticket is considered overdue when the current time passes its SLA due date.
11. Authentication uses Django's built-in User model and Groups for role management.

---

## 3. Architecture

The application follows Django's Model-View-Template (MVT) architecture.

### Models

The main models are:

- `Ticket`
- `Comment`
- `TicketActivity`

The `Ticket` model stores the main support request information.

The `Comment` model stores communication related to a ticket.

The `TicketActivity` model records important changes such as:
- Status changes
- Priority changes
- Ticket assignment

### Views

Django views handle:

- Authentication
- Ticket creation
- Student ticket listing
- Ticket details
- Staff ticket management
- Ticket updates
- Manager dashboard

### Templates

Separate HTML templates provide interfaces for:

- Login
- Ticket creation
- Student ticket list
- Ticket details
- Staff ticket management
- Ticket updates
- Manager dashboard

### Role-based access

Django Groups are used for:

- Student
- Staff
- Manager

Views check the user's role before allowing access to role-specific functionality.

---

## 4. SLA and Ageing

SLA is calculated based on ticket priority.

| Priority | SLA |
|----------|-----|
| High | 1 day |
| Medium | 2 days |
| Low | 3 days |

Ticket ageing is calculated using the ticket creation time and the current time.

The staff interface displays whether a ticket is:

- On Track
- Overdue

This helps staff identify tickets that require attention.

---

## 5. Activity Tracking

Important ticket changes are recorded using `TicketActivity`.

For example:

- Status changed from Open to In Progress
- Priority changed from Medium to High
- Ticket assigned to a staff member

This provides a basic audit trail and helps users understand the history of a ticket.

---

## 6. Trade-offs

### Django built-in User model

The project uses Django's built-in `User` model instead of creating a custom user model.

**Reason:**
The assignment requires role-based access and authentication, and Django's existing authentication system provides the required functionality without unnecessary complexity.

**Trade-off:**
More advanced user-specific fields would require extending or replacing the current user structure.

### Django Groups for roles

Groups are used for Student, Staff and Manager roles.

**Reason:**
This provides a simple way to implement role-based access control.

**Trade-off:**
More complex permission structures may require Django permissions or a dedicated role/permission model.

### SLA calculation

SLA is based on fixed priority-based durations.

**Reason:**
It provides a simple and understandable SLA mechanism for the prototype.

**Trade-off:**
The current implementation does not account for working hours, holidays or different SLA policies for different categories.

### SQLite

SQLite is used as the database for the prototype.

**Reason:**
It is simple to configure and sufficient for local development and demonstration.

**Trade-off:**
A production deployment with higher concurrency would typically require a production database system.

---

## 7. Validation and Edge Cases

The implementation considers several edge cases:

- Unauthenticated users are redirected to the login page.
- Students can access only their own tickets.
- Students cannot access staff or manager functionality.
- Staff cannot access manager functionality.
- Tickets without an assigned staff member are supported.
- Tickets without a stored SLA due date can still have their SLA status calculated.
- Resolved tickets store a resolution timestamp.
- Changing ticket status, priority or assignment creates an activity record.
- Invalid login credentials display an error message.

---

## 8. Technology Stack

- Python
- Django
- SQLite
- HTML
- CSS
- Django Templates
- Git
- GitHub

---

## 9. Future Improvements

Possible improvements for a production version include:

- Email or in-app notifications
- Advanced search and filtering
- Pagination for large ticket lists
- File attachments
- More detailed reporting
- Configurable SLA policies
- Working-hour based SLA calculation
- Automated escalation for overdue tickets
- More granular permissions
- Production database such as PostgreSQL