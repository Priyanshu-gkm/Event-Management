from django.urls import path, include
from accounts import views
from . import views as api_views

urlpatterns = [
    path("accounts/", include("accounts.urls")),
    path("login/", views.LoginView.as_view(), name="user_login"),
    path("logout/", views.LogoutView.as_view(), name="user_logout"),
    path("events/", include("events.urls")),
    path("ticket-types/", include("tickets.ticket_type_urls")),
    path("tickets/", include("tickets.urls")),
    path("wishlist/", include("wishlist.urls")),
    # path("test_create/", api_views.create_sample_tickets),
    # path("test_dict/", api_views.create_notification),
    # path("test_model/", api_views.send_mail_to_attendees),
]
