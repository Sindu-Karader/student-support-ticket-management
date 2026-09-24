from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import TicketForm, CommentForm, StaffTicketForm
from .models import Ticket, Comment, TicketActivity
from django.contrib.auth.models import Group
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth import authenticate, login


def user_has_role(user, role):
    return user.groups.filter(name=role).exists()

def custom_login(request):

    if request.user.is_authenticated:

        if user_has_role(request.user, 'Student'):
            return redirect('create_ticket')

        elif user_has_role(request.user, 'Staff'):
            return redirect('staff_tickets')

        elif user_has_role(request.user, 'Manager'):
            return redirect('manager_dashboard')

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            if user_has_role(user, 'Student'):
                return redirect('create_ticket')

            elif user_has_role(user, 'Staff'):
                return redirect('staff_tickets')

            elif user_has_role(user, 'Manager'):
                return redirect('manager_dashboard')

            else:
                return redirect('login')

        else:

            return render(
                request,
                'tickets/login.html',
                {
                    'error': 'Invalid username or password.'
                }
            )

    return render(
        request,
        'tickets/login.html'
    )

@login_required
def create_ticket(request):

    if not user_has_role(request.user, 'Student'):
        return redirect('login')

    if request.method == 'POST':
        form = TicketForm(request.POST)

        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.student = request.user

        if ticket.priority == 'high':
            ticket.due_date = timezone.now() + timedelta(days=1)

        elif ticket.priority == 'medium':
            ticket.due_date = timezone.now() + timedelta(days=2)

        else:
            ticket.due_date = timezone.now() + timedelta(days=3)

        ticket.save()

        return redirect('ticket_success')

    else:
        form = TicketForm()

    return render(request, 'tickets/create_ticket.html', {'form': form})


def ticket_success(request):
    return render(request, 'tickets/ticket_success.html')


@login_required
def my_tickets(request):

    if not user_has_role(request.user, 'Student'):
        return redirect('login')

    tickets = Ticket.objects.filter(
        student=request.user
    ).order_by('-created_at')

    return render(
        request,
        'tickets/my_tickets.html',
        {'tickets': tickets}
    )


@login_required
def ticket_detail(request, ticket_id):

    if not user_has_role(request.user, 'Student'):
        return redirect('login')

    ticket = Ticket.objects.get(
        id=ticket_id,
        student=request.user
    )

    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.ticket = ticket
            comment.user = request.user
            comment.save()

            return redirect(
                'ticket_detail',
                ticket_id=ticket.id
            )

    else:
        form = CommentForm()

    activities = ticket.activities.all().order_by('-created_at')

    return render(
        request,
        'tickets/ticket_detail.html',
        {
            'ticket': ticket,
            'form': form,
            'activities': activities
        }
    )


@login_required
def staff_tickets(request):

    if not user_has_role(request.user, 'Staff'):
        return redirect('login')

    tickets = Ticket.objects.all().order_by('-created_at')

    now = timezone.now()

    for ticket in tickets:

        if ticket.due_date is None:

            if ticket.priority == 'high':
                ticket.due_date = ticket.created_at + timedelta(days=1)

            elif ticket.priority == 'medium':
                ticket.due_date = ticket.created_at + timedelta(days=2)

            else:
                ticket.due_date = ticket.created_at + timedelta(days=3)

        ticket.age_days = (now - ticket.created_at).days

        if now > ticket.due_date:
            ticket.sla_status = 'Overdue'
        else:
            ticket.sla_status = 'On Track'

    return render(
        request,
        'tickets/staff_tickets.html',
        {'tickets': tickets}
    )

@login_required
def update_ticket(request, ticket_id):

    if not user_has_role(request.user, 'Staff'):
        return redirect('login')

    staff_group = Group.objects.get(name='Staff')

    if staff_group not in request.user.groups.all():
        return redirect('my_tickets')

    ticket = Ticket.objects.get(id=ticket_id)

    if request.method == 'POST':

        old_status = ticket.get_status_display()
        old_priority = ticket.get_priority_display()
        old_assigned_to = ticket.assigned_to

        form = StaffTicketForm(
            request.POST,
            instance=ticket
        )

        if form.is_valid():

            updated_ticket = form.save()

            # Set resolved time
            if (
                updated_ticket.status == 'resolved'
                and ticket.resolved_at is None
            ):
                updated_ticket.resolved_at = timezone.now()
                updated_ticket.save()

            # Clear resolved time if ticket is moved back
            elif (
                updated_ticket.status != 'resolved'
                and ticket.resolved_at is not None
            ):
                updated_ticket.resolved_at = None
                updated_ticket.save()

            new_status = updated_ticket.get_status_display()
            new_priority = updated_ticket.get_priority_display()

            if old_status != new_status:

                TicketActivity.objects.create(
                    ticket=ticket,
                    user=request.user,
                    action='Status Changed',
                    description=(
                        f'Status changed from '
                        f'{old_status} to {new_status}'
                    )
                )

            if old_priority != new_priority:

                TicketActivity.objects.create(
                    ticket=ticket,
                    user=request.user,
                    action='Priority Changed',
                    description=(
                        f'Priority changed from '
                        f'{old_priority} to {new_priority}'
                    )
                )

            if old_assigned_to != updated_ticket.assigned_to:

                if updated_ticket.assigned_to:
                    assigned_name = updated_ticket.assigned_to.username
                else:
                    assigned_name = 'Nobody'

                TicketActivity.objects.create(
                    ticket=ticket,
                    user=request.user,
                    action='Ticket Assigned',
                    description=(
                        f'Ticket assigned to '
                        f'{assigned_name}'
                    )
                )

            return redirect('staff_tickets')

    else:

        form = StaffTicketForm(
            instance=ticket
        )

    return render(
        request,
        'tickets/update_ticket.html',
        {
            'ticket': ticket,
            'form': form
        }
    )

@login_required
def manager_dashboard(request):

    if not user_has_role(request.user, 'Manager'):
        return redirect('login')

    total_tickets = Ticket.objects.count()

    open_tickets = Ticket.objects.filter(
        status='open'
    ).count()

    in_progress_tickets = Ticket.objects.filter(
        status='in_progress'
    ).count()

    pending_tickets = Ticket.objects.filter(
        status='pending'
    ).count()

    resolved_tickets = Ticket.objects.filter(
        status='resolved'
    ).count()

    closed_tickets = Ticket.objects.filter(
        status='closed'
    ).count()

    high_priority_tickets = Ticket.objects.filter(
        priority='high'
    ).count()

    now = timezone.now()

    overdue_tickets = []

    tickets = Ticket.objects.all()

    for ticket in tickets:

        if ticket.due_date:

            if now > ticket.due_date:
                overdue_tickets.append(ticket)

        else:

            if ticket.priority == 'high':
                due_date = ticket.created_at + timedelta(days=1)

            elif ticket.priority == 'medium':
                due_date = ticket.created_at + timedelta(days=2)

            else:
                due_date = ticket.created_at + timedelta(days=3)

            if now > due_date:
                overdue_tickets.append(ticket)

    staff_group = Group.objects.get(name='Staff')

    staff_users = staff_group.user_set.all()

    staff_workload = []

    for staff in staff_users:

        assigned_count = Ticket.objects.filter(
            assigned_to=staff
        ).count()

        staff_workload.append({
            'username': staff.username,
            'assigned_count': assigned_count
        })

    context = {
        'total_tickets': total_tickets,
        'open_tickets': open_tickets,
        'in_progress_tickets': in_progress_tickets,
        'pending_tickets': pending_tickets,
        'resolved_tickets': resolved_tickets,
        'closed_tickets': closed_tickets,
        'high_priority_tickets': high_priority_tickets,
        'overdue_tickets': overdue_tickets,
    }

    return render(
        request,
        'tickets/manager_dashboard.html',
        context
    )