# event_manager/urls.py
from django.urls import path
from accounts import views

urlpatterns = [
   path('', views.AccountAPIView.as_view()),
    path('<int:pk>/', views.AccountAPIView.as_view()),
]