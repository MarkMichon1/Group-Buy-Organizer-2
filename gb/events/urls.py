from django.urls import path

from events import pdf_views, views

urlpatterns = [
    path('<int:event_id>/chat/', views.chat, name='events-chat'),
    path('<int:event_id>/chat/<int:comment_id>/delete/', views.comment_delete, name='events-chat-delete-comment'),
    path('create/', views.create_event, name='events-create'),
    path('<int:event_id>/', views.event, name='events-event'),
    path('<int:event_id>/settings/', views.event_settings, name='events-settings'),
    path('<int:event_id>/close/', views.close_event, name='events-close'),
    path('<int:event_id>/delete/', views.delete_event, name='events-delete'),
    path('<int:event_id>/item/<int:item_id>/', views.item, name='events-item'),
    path('<int:event_id>/item/<int:item_id>/edit/', views.edit_item, name='events-item-edit'),
    path('<int:event_id>/item/<int:item_id>/delete/', views.delete_item, name='events-item-delete'),
    path('<int:event_id>/item/<int:item_id>/chat/<int:chat_id>/delete/', views.delete_item_chat, name='events-item-chat-delete'),
    path('<int:event_id>/item/<int:item_id>/youtube_posting/<int:youtube_id>/delete/', views.delete_item_youtube, name='events-item-youtube-delete'),
    path('<int:event_id>/item/<int:item_id>/case-split/<int:case_split_id>/', views.case_split, name='events-case-split'),
    path('<int:event_id>/item/<int:item_id>/case-split/<int:case_split_id>/commit/<int:commit_id>/delete/', views.case_split_commit_delete, name='events-case-split-commit-delete'),
    path('<int:event_id>/item/<int:item_id>/case-split/<int:case_split_id>/delete/', views.case_split_delete, name='events-case-split-delete'),
    path('<int:event_id>/leave/', views.leave_event, name='events-leave'),
    path('<int:event_id>/manage-payments/', views.manage_payments, name='events-manage-payments'),
    path('<int:event_id>/manage-users/', views.manage_users, name='events-manage-users'),
    path('<int:event_id>/my-order/<int:user_id>/', views.my_order, name='events-my-order'),
    path('<int:event_id>/my-order/<int:user_id>/pdf/', pdf_views.my_order_pdf, name='events-my-order-pdf'),
    path('<int:event_id>/order-breakdown/', views.order_breakdown, name='events-order-breakdown'),
    path('<int:event_id>/order-breakdown/pdf/', pdf_views.order_breakdown_pdf, name='events-order-breakdown-pdf'),
    path('<int:event_id>/remove-participant/<int:user_id>/', views.remove_participant, name='events-remove-participant'),
    path('<int:event_id>/summary/', views.event_order_summary, name='events-order-summary'),
    path('<int:event_id>/summary/pdf/', pdf_views.event_order_summary_pdf, name='events-order-summary-pdf'),
    path('<int:event_id>/toggle-organizer/<int:user_id>/', views.toggle_organizer, name='events-toggle-organizer'),
    path('<int:event_id>/toggle-payment/<int:target_membership_id>/', views.toggle_payment, name='events-toggle-payment')
]