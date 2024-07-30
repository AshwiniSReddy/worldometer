from django.urls import path
from . import views

urlpatterns = [
    path('members/', views.members, name='members'),
    path('worldometer_expenditure_view/', views.worldometer_expenditure_view, name='worldometer_expenditure_view'),
]