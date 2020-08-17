from django.urls import path
from billing_sessions import views

urlpatterns = [
    path("home/", views.Home.as_view(), name="home"),
    path("calendar/<int:id>/", views.Home.as_view(), name="calendar"),
    path("past_sessions/", views.PastSessions.as_view(), name="past_sessions"),
]
