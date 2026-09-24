from django.db import models
from django.contrib.auth.models import User

class Ticket(models.Model):
    CATEGORY_CHOICES = [
        ('fees','Fees'),
        ('attendance','Attendance'),
        ('id_card','ID Card'),
        ('documents','Documents'),
        ('certifications','Certifications'),
        ('others','Others'),
    ]

    PRIORITY_CHOICES = [
        ('low','Low'),
        ('medium','Medium'),
        ('high','High'),
    ]

    STATUS_CHOICES = [
        ('open','Open'),
        ('in_progress','In Progress'),
        ('pending','Pending'),
        ('resolved','Resolved'),
        ('closed','Closed')
    ]

    student = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='created_tickets'
    )

    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=20,
                                choices=CATEGORY_CHOICES
    )

    priority = models.CharField(
        max_length=15,
        choices=PRIORITY_CHOICES,
        default='medium'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='open'
    )

    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_tickets'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    due_date = models.DateTimeField(null=True, blank=True)

    resolved_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title


class Comment(models.Model):

    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    message = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"Comment on {self.ticket.title}"


class TicketActivity(models.Model):

    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        related_name='activities'
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    action = models.CharField(max_length=100)

    description = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.action} - {self.ticket.title}"
