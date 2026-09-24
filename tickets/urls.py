from django.urls import path
from .import views

urlpatterns = [
    path('create/',views.create_ticket, name='create_ticket'),
    path('success/',views.ticket_success,name='ticket_success'),
    path('my-tickets/',views.my_tickets,name='my_tickets'),
    path('ticket/<int:ticket_id>/',views.ticket_detail,name='ticket_detail'),
    path('staff-tickets/',views.staff_tickets,name='staff_tickets'),
    path('ticket/<int:ticket_id>/update/',views.update_ticket,name='update_ticket'),
    path('manager-dashboard/',views.manager_dashboard,name='manager_dashboard'),
] 