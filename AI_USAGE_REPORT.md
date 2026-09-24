# AI Usage Report

## 1. AI Tool Used

ChatGPT

AI was used as a development assistant during the implementation of the Student Support & Ticket Management system.

---

## 2. What I Asked AI

I used AI assistance for:

- Understanding the assignment requirements
- Planning the Django application structure
- Designing the Ticket, Comment and TicketActivity models
- Implementing Django forms and views
- Implementing role-based access using Django Groups
- Implementing authentication and login redirection
- Implementing SLA and ticket ageing logic
- Implementing ticket activity tracking
- Creating the manager dashboard
- Debugging Django errors and access-control issues
- Improving the project documentation and README
- Reviewing edge cases and testing scenarios

---

## 3. Most Useful Prompt

One of the most useful prompts was to explain the assignment requirements and ask for a step-by-step implementation approach suitable for a beginner.

The AI was also asked to provide complete updated Django code when changes were required so that the implementation could be tested directly.

---

## 4. Code Generated With AI Assistance

AI assistance was used for parts of:

- Django models
- Django forms
- Django views
- URL configuration
- HTML templates
- CSS styling
- Role-based access checks
- SLA calculation
- Ticket activity tracking
- Manager dashboard logic

The generated code was reviewed and tested before being included in the project.

---

## 5. Code Modified by Me

I modified and integrated the generated code according to the actual project structure and requirements.

Examples include:

- Connecting the views to the project's existing URLs and templates
- Configuring Django Groups for Student, Staff and Manager roles
- Creating the project-specific management command for roles
- Creating users and assigning them to the appropriate groups
- Adjusting login redirection according to user role
- Testing student, staff and manager access
- Modifying templates and CSS
- Testing ticket creation and ticket management workflows
- Updating documentation based on the implemented features

---

## 6. Incorrect or Problematic AI Output

During development, some implementation issues were identified during testing.

### Issue 1: Logout request method

The initial logout implementation resulted in a `405 Method Not Allowed` response when logout was accessed using a GET request.

### How I identified it

I tested the logout functionality in the browser and observed the HTTP 405 response.

### How I fixed it

The logout functionality was changed to use a POST form with CSRF protection.

---

### Issue 2: Role-based access

Initially, users could manually enter URLs for pages belonging to other roles.

For example, a student could attempt to access staff or manager pages directly.

### How I identified it

I tested the application by logging in with different role accounts and manually changing the URL.

### How I fixed it

Role checks were added to the relevant views using Django Groups.

The application now verifies whether the logged-in user belongs to the required role before displaying role-specific pages.

---

### Issue 3: Login redirection

The initial login configuration redirected every authenticated user to the student ticket creation page.

This caused problems for Staff users because the staff account was redirected to a student-only page.

### How I identified it

I tested login using the Staff account and observed that it was redirected to the wrong page.

### How I fixed it

A custom login view was implemented to redirect users according to their role:

- Student → Ticket creation
- Staff → Staff ticket list
- Manager → Manager dashboard

---

### Issue 4: Student ticket access

The ticket detail page initially required additional access-control testing to ensure that students could not view another student's ticket by changing the ticket ID in the URL.

### How I identified it

I manually changed the ticket ID in the browser URL while logged in as a student.

### How I fixed it

The ticket lookup was restricted using both the ticket ID and the logged-in student.

This ensures that a student can view only their own tickets.

---

## 7. How AI-Generated Code Was Validated

AI-generated code was not accepted without testing.

Validation was performed by:

- Running Django system checks
- Running database migrations
- Starting the Django development server
- Testing login with different roles
- Creating tickets as a student
- Viewing student tickets
- Updating tickets as staff
- Testing ticket assignment
- Testing priority and status changes
- Testing SLA and overdue calculations
- Testing manager dashboard statistics
- Testing access restrictions by manually changing URLs
- Checking Git changes before committing
- Testing the final application in the browser

---

## 8. My Role in the Implementation

AI was used as a development and learning assistant.

I reviewed, integrated, modified and tested the generated suggestions against the actual assignment requirements and application behavior.

When an issue was found during testing, I investigated the behavior and modified the implementation accordingly.