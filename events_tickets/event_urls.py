from django.urls import path
from events_tickets import views

urlpatterns = [
    # path("list/",views.EventListAPIView.as_view(),name="list-events"),
    path("",views.EventListCreate.as_view(),name="create-event"),
]