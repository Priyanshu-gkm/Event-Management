from django.urls import path
from events_tickets import views

urlpatterns = [
    path("",views.EventListCreate.as_view(),name="LC-event"),
    path("<int:pk>/",views.EventRUD.as_view(),name="RUD-event"),
]