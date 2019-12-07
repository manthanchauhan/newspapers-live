from django.urls import path
from plans import views

urlpatterns = [
    path('create_plan/', views.CreatePlan.as_view(), name='create_plan'),
    path('edit/', views.EditPlan.as_view(), name='edit_plan'),
]
