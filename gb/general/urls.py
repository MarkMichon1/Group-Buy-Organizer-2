from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='general-home'),
    path('about/', views.about, name='general-about'),
    path('updates/', views.updates, name='general-updates'),

]