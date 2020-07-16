from django.urls import path

from . import views

urlpatterns = [
    path('create/', views.create_event, name='events-create'),
    path('<uuid:event_id>/', views.event, name='events-event'),
    path('<uuid:event_id>/settings/', views.event_settings, name='events-settings'),
    path('<uuid:event_id>/delete/', views.delete_event, name='events-delete'),
    path('<uuid:event_id>/item/<uuid:item_id>/', views.item, name='events-item'),
    path('<uuid:event_id>/item/<uuid:item_id>/edit/', views.edit_item, name='events-item-edit'),
    path('<uuid:event_id>/item/<uuid:item_id>/delete/', views.delete_item, name='events-item-delete'),
    path('<uuid:event_id>/item/<uuid:item_id>/case-split/<uuid:case_split_id>/', views.case_split, name='events-case-split'),
    path('<uuid:event_id>/leave/', views.leave_event, name='events-leave'),
    path('<uuid:event_id>/manage-payments/', views.manage_payments, name='events-manage-payments'),
    path('<uuid:event_id>/manage-users/', views.manage_users, name='events-manage-users'),
    path('<uuid:event_id>/summary/', views.event_order_summary, name='events-order-summary'),
    path('<uuid:event_id>/order-breakdown/', views.order_breakdown, name='events-order-breakdown'),
    path('<uuid:event_id>/my-order/<uuid:user_id>/', views.my_order, name='events-my-order'),
    path('<uuid:event_id>/chat/', views.chat, name='events-chat'),
    path('<uuid:event_id>/chat/<int:comment_id>/delete/', views.comment_delete, name='events-chat-delete-comment')
]
#todo organize