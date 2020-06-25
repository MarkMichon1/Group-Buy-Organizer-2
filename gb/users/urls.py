from django.urls import path

from . import views

urlpatterns = [
    path('toggle-nightmode/', views.toggle_night_mode, name='users-toggle-nightmode'),


]