from django.urls import path
from plans.views import CreatePlan

urlpatterns = [
    path('new_plan', CreatePlan.as_view(), name='create_plan'),
]
