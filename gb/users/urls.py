from django.urls import path

from . import views

urlpatterns = [
    path('toggle-nightmode/', views.toggle_night_mode, name='users-toggle-nightmode'),
    path('activate/<uuid:pk>/', views.activate_account, name='users-activate')

]