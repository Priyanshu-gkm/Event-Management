from django.urls import path
from events_tickets import views

urlpatterns = [
    path("",views.TicketTypeLC.as_view(),name="LC-ticket"),
    path("<int:pk>/",views.TicketTypeRUD.as_view(),name="RUD-ticket"),
]