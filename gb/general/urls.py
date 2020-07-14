from django.urls import path

from general import views

urlpatterns = [
    path('', views.home, name='general-home'),
    path('about/', views.about, name='general-about'),
    path('donate/', views.donate, name='general-donate'),
    path('statistics/', views.statistics, name='general-statistics'),
    path('updates/', views.BlogListView.as_view(), name='general-updates'),
    path('updates/new/', views.BlogCreateView.as_view(), name='general-updates-create'),
    path('updates/<int:pk>/update/', views.BlogUpdateView.as_view(), name='general-updates-update'),
    path('updates/<int:pk>/delete/', views.BlogDeleteView.as_view(), name='general-updates-delete'),
    path('secret-initialization/', views.secret_service_initialization, name='general-secret-initialization'),

]