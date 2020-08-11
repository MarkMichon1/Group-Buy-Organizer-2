from django.urls import path

from . import api_views, views

urlpatterns = [
path('', views.pm_inbox, name='personal_messages-inbox'),
path('sentbox/', views.pm_sentbox, name='personal_messages-sentbox'),
path('compose/', views.pm_compose, name='personal_messages-compose'),
path('<int:pk>/', views.pm_detail, name='personal_messages-detail'),

]