from django.urls import path

from . import views

urlpatterns = [
    path('create/', views.create_event, name='events-create'),
    path('<uuid:pk>/', views.event, name='events-event'),
    path('<uuid:pk>/edit/', views.edit_event, name='events-edit'),
    path('<uuid:pk>/delete/', views.delete_event, name='events-delete'),
    path('<uuid:pk>/item/<uuid:item_id>/', views.item, name='events-item'),
    path('<uuid:pk>/item/<uuid:item_id>/edit/', views.edit_item, name='events-item-edit'),
    path('<uuid:pk>/item/<uuid:item_id>/delete/', views.delete_item, name='events-item-delete'),
    path('<uuid:pk>/item/<uuid:item_id>/case-split/', views.case_split, name='events-case-split'),
    path('<uuid:pk>/manage-payments/', views.manage_payments, name='events-manage-payments'),
    path('<uuid:pk>/summary/', views.summary, name='events-summary'),
    path('<uuid:pk>/user-breakdown/', views.user_breakdown, name='events-user-breakdown'),
    path('<uuid:pk>/my-order/', views.my_order, name='events-my-order'),
    path('<uuid:pk>/chat/', views.chat, name='events-chat'),
]