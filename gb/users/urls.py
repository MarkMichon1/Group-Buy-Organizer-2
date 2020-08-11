from django.urls import path

from . import api_views, views

urlpatterns = [
    path('activate/<uuid:pk>/', views.activate_account, name='users-activate'),
    path('toggle-explanations/', views.toggle_explanations, name='users-toggle-explanations'),
    path('profile/<str:targetted_user_name>', views.profile, name='users-profile'),
    path('toggle-nightmode/', views.toggle_night_mode, name='users-toggle-nightmode'),

    path('api/user-autocomplete/', api_views.api_user_autocomplete, name='users-api-user-autocomplete')
]