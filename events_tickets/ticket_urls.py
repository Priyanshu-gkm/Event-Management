from django.urls import path
from events_tickets import views

urlpatterns = [
    path("types",views.TicketTypeLC.as_view(),name="ticket-types")
]