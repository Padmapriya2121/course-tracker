from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_courses),
    path('enroll/', views.enroll),
]