from django.urls import path , include

urlpatterns = [
    path("accounts/",include('accounts.urls')),
    path("events/",include("events_tickets.event_urls")),
    path("tickets/",include("events_tickets.ticket_urls")),
]