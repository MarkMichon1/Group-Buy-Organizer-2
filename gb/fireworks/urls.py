from django.urls import path

from . import api_views, views

urlpatterns = [
    path('', views.firework_home, name='fireworks-home'),
    path('add/', views.add_firework, name='fireworks-add'),
    path('categories', views.category, name='fireworks-categories'),
    path('category/<slug:category_slug>/', views.category, name='fireworks-category'),
    path('category/<slug:category_slug>/<slug:firework_slug>/', views.firework_detail, name='fireworks-detail'),
    path('favorites/<int:pk>/', views.favorites, name='fireworks-favorites'),
    path('manufacturer/<slug:manufacturer_slug>/', views.manufacturer, name='fireworks-manufacturer'),
    path('manufacturers/', views.manufacturers, name='fireworks-manufacturers'),
]
