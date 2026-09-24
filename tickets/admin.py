from django.contrib import admin
from .models import Ticket, Comment, TicketActivity


admin.site.register(Ticket)
admin.site.register(Comment)
admin.site.register(TicketActivity)