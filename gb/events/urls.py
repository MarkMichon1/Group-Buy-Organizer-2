from django.urls import path

from . import views

urlpatterns = [
    path('create/', views.create_event, name='events-create'),
    path('<uuid:id>/', views.event, name='events-event'),
    path('<uuid:id>/edit/', views.edit_event, name='events-edit'),
    path('<uuid:id>/delete/', views.delete_event, name='events-delete'),
    path('<uuid:id>/item/<uuid:item_id>/', views.item, name='events-item'),
    path('<uuid:id>/item/<uuid:item_id>/edit/', views.edit_item, name='events-item-edit'),
    path('<uuid:id>/item/<uuid:item_id>/delete/', views.delete_item, name='events-item-delete'),
    path('<uuid:id>/case-split/', views.case_split, name='events-case-split'),
    path('<uuid:id>/manage-payments/', views.manage_payments, name='events-manage-payments'),
    path('<uuid:id>/summary/', views.summary, name='events-summary'),
    path('<uuid:id>/user-breakdown/', views.user_breakdown, name='events-user-breakdown'),
    path('<uuid:id>/my-order/', views.my_order, name='events-my-order'),
    path('<uuid:id>/chat/', views.chat, name='events-chat'),
]