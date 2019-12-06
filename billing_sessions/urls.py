from django.urls import path
from billing_sessions import views

urlpatterns = [
    path('home/', views.Home.as_view(), name='home')
]
