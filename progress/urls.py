from django.urls import path
from . import views

urlpatterns = [
    path('complete/', views.complete_lesson),
    path('', views.get_progress),
]