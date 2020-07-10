from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='general-home'),
    path('about/', views.about, name='general-about'),
    path('donate/', views.donate, name='general-donate'),
    path('updates/', views.updates, name='general-updates'),
    path('secret-initialization/', views.secret_service_initialization, name='general-secret-initialization'),

]