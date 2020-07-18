from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import get_object_or_404, HttpResponseRedirect, redirect, render
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from events.forms import AddUserForm, CommentCreateForm, EventCreateForm
from events.models import CaseBuy, CasePieceCommit, CaseSplit, Event, EventComment, EventMembership, Item
from events.utilities import event_auth_checkpoint
from users.models import User

@login_required
def create_event(request):
    if request.method == 'POST':
        form = EventCreateForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['name']
            description = form.cleaned_data['description']
            event = Event(name=title, description=description, created_by=request.user)
            event.save()
            membership = EventMembership(user=request.user, event=event, is_organizer=True, is_creator=True)
            membership.save()
            messages.success(request, f"Event successfully created!  Click your event Event Settings button in the organizer toolbar to add more members.")
            return redirect('general-home')
    else:
        context = {
            'form' : EventCreateForm(),
            'title' : 'New Event'
        }
        return render(request, 'events/create_event.html', context=context)

@login_required
def event(request, event_id):
    # Note- until I find a proper way to deal with this, these three lines will be in all event views requiring auth.
    event, membership, is_valid = event_auth_checkpoint(event_id=event_id, request=request)
    if is_valid == False:
        return redirect('general-home')

    context = {'title' : event.name,
               'event' : event,
               'membership' : membership}
    return render(request, 'events/event.html', context=context)


@login_required
def event_settings(request, event_id):
    event, membership, is_valid = event_auth_checkpoint(event_id=event_id, request=request, organizer=True)
    if is_valid == False:
        return redirect('general-home')
    context = {
        'event' : event,
        'title' : f'Event Settings'
    } #
    return render(request, 'events/event_settings.html', context=context)


@login_required
def event_toggle_lock(request, event_id):
    event, membership, is_valid = event_auth_checkpoint(event_id=event_id, request=request, organizer=True)
    if is_valid == False:
        return redirect('general-home')


@login_required
def event_toggle_close(request, event_id):
    event, membership, is_valid = event_auth_checkpoint(event_id=event_id, request=request, organizer=True)
    if is_valid == False:
        return redirect('general-home')


@login_required
def leave_event(request, event_id):
    event, membership, is_valid = event_auth_checkpoint(event_id=event_id, request=request)
    if is_valid == False:
        return redirect('general-home')
    membership.delete()
    messages.success(request, 'You have left the event!')
    return redirect('general-home')


@login_required
def delete_event(request, event_id):
    event, membership, is_valid = event_auth_checkpoint(event_id=event_id, request=request, organizer=True)
    if is_valid == False:
        return redirect('general-home')
    if membership.is_creator or request.user.is_staff:
        name = event.name
        event.delete()
        messages.success(request, f"Poof!  Event '{name}' has been deleted.")
        return redirect('general-home')
    else:
        messages.warning(request, 'Access denied.')
        return redirect('general-home')


@login_required
def item(request, event_id, item_id):
    event, membership, is_valid = event_auth_checkpoint(event_id=event_id, request=request)
    if is_valid == False:
        return redirect('general-home')
    item = get_object_or_404(Item, pk=item_id)
    context = {
        'event': event,
        'item': item,
        'title': item.name
    }
    return render(request, 'events/item.html', context=context)


@login_required
def edit_item(request, event_id, item_id):
    event, membership, is_valid = event_auth_checkpoint(event_id=event_id, request=request)
    if is_valid == False:
        return redirect('general-home')
    item = get_object_or_404(Item, pk=item_id)
    context = {
        'event': event,
        'item': item,
        'title': f'Edit {item.name}'
    }
    return render(request, 'general/object_create_update.html', context=context)


@login_required
def delete_item(request, event_id, item_id):
    event, membership, is_valid = event_auth_checkpoint(event_id=event_id, request=request)
    if is_valid == False:
        return redirect('general-home')
    item = get_object_or_404(Item, pk=item_id)


@login_required
def case_split(request, event_id, item_id, case_split_id):
    event, membership, is_valid = event_auth_checkpoint(event_id=event_id, request=request)
    if is_valid == False:
        return redirect('general-home')
    item = get_object_or_404(Item, pk=item_id)
    case_split = get_object_or_404(CaseSplit, pk=case_split_id)
    context = {
        'event': event,
        'item': item,
        'title': f'{item.name} Case Split'
    }
    return render(request, 'events/case_split.html', context=context)


@login_required
def manage_payments(request, event_id):
    event, membership, is_valid = event_auth_checkpoint(event_id=event_id, request=request, organizer=True)
    if is_valid == False:
        return redirect('general-home')

    memberships = EventMembership.objects.filter(event=event)

    context = {
        'event': event,
        'memberships': memberships,
        'title': 'Manage Payments'
    }
    return render(request, 'events/manage_payments.html', context=context)


@login_required
def toggle_payment(request, event_id, target_membership_id):
    event, your_membership, is_valid = event_auth_checkpoint(event_id=event_id, request=request, organizer=True)
    if is_valid == False:
        return redirect('general-home')
    membership = get_object_or_404(EventMembership, pk=target_membership_id)
    membership.has_paid = not membership.has_paid
    membership.save()
    if membership.has_paid:
        messages.success(request, f'{membership.user.username} has been marked as paid!')
        return redirect('events-manage-payments', event_id=event_id)
    else:
        messages.success(request, f'{membership.user.username} has been marked as unpaid!')
        return redirect('events-manage-payments', event_id=event_id)


@login_required
def manage_users(request, event_id):
    event, your_membership, is_valid = event_auth_checkpoint(event_id=event_id, request=request, organizer=True)
    if is_valid == False:
        return redirect('general-home')

    memberships = EventMembership.objects.filter(event=event)
    add_user_form = AddUserForm()

    if request.method == 'POST':
        form = AddUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            try:
                user = User.objects.get(username=username)
                membership = EventMembership(event=event, user=user)
                membership.save()
                messages.success(request, 'User successfully added.')
                return redirect('events-manage-users', event_id=event_id)
            except:
                messages.warning(request, f"User '{username}' does not exist.  Maybe it is misspelled?")
                return redirect('events-manage-users', event_id=event_id)

    else:
        context = {
            'add_user_form': add_user_form,
            'event': event,
            'memberships': memberships,
            'title': 'Manage Users',
            'your_membership': your_membership
        }
        return render(request, 'events/manage_users.html', context=context)


@login_required
def toggle_organizer(request, event_id, user_id):
    event, membership, is_valid = event_auth_checkpoint(event_id=event_id, request=request, organizer=True)
    if is_valid == False:
        return redirect('general-home')
    if request.user.is_staff or membership.is_creator:
        target_membership = EventMembership.objects.get(user__id=user_id, event__id=event_id)
        target_membership.is_organizer = not target_membership.is_organizer
        target_membership.save()
        if target_membership.is_organizer:
            messages.success(request, f'Organizer status enabled for {target_membership.user.username}.')
        else:
            messages.success(request, f'Organizer status disabled for {target_membership.user.username}.')
        return redirect('events-manage-users', event_id=event.id)
    else:
        messages.warning(request, 'Access denied.')
        return redirect('general-home')


@login_required
def remove_participant(request, event_id, user_id):
    event, membership, is_valid = event_auth_checkpoint(event_id=event_id, request=request, organizer=True)
    if is_valid == False:
        return redirect('general-home')
    if request.user.is_staff or membership.is_creator:
        target_membership = EventMembership.objects.get(user__id=user_id, event__id=event_id)
        username = target_membership.user.username
        target_membership.delete()
        messages.success(request, f'{username} removed from event.')
        return redirect('events-manage-users', event_id=event.id)

    else:
        messages.warning(request, 'Access denied.')
        return redirect('general-home')


@login_required
def event_order_summary(request, event_id):
    event, membership, is_valid = event_auth_checkpoint(event_id=event_id, request=request)
    if is_valid == False:
        return redirect('general-home')
    context = {
        'event': event,
        'title': 'Event Order Summary'
    }
    return render(request, 'events/event_order_summary.html', context=context)

@login_required
def order_breakdown(request, event_id):
    event, membership, is_valid = event_auth_checkpoint(event_id=event_id, request=request)
    if is_valid == False:
        return redirect('general-home')
    context = {
        'event': event,
        'title': 'Order Breakdown By User',
    }
    return render(request, 'events/user _breakdown.html', context=context)


@login_required
def my_order(request, event_id, user_id):
    event, membership, is_valid = event_auth_checkpoint(event_id=event_id, request=request)
    if is_valid == False:
        return redirect('general-home')
    user = get_object_or_404(User, pk=user_id)
    context = {
        'event': event,
        'title': f"{user.username}'s Order",
        'user': user
    }
    return render(request, 'events/my_order.html', context=context)


@login_required
def chat(request, event_id):
    event, membership, is_valid = event_auth_checkpoint(event_id=event_id, request=request)
    if is_valid == False:
        return redirect('general-home')

    if request.method == 'POST':
        form = CommentCreateForm(request.POST)
        if form.is_valid():
            comment = form.cleaned_data['comment']
            event_comment = EventComment(author=request.user, event=event, membership=membership, comment=comment)
            event_comment.save()
            messages.success(request, 'Comment posted!')
            return redirect('events-chat', event_id=event_id)
    else:
        event_comments = EventComment.objects.filter(event=event)
        paginator = Paginator(event_comments, 50)
        page_number = request.GET.get('page')
        page_comments = paginator.get_page(page_number)

        context = {
            'event' : event,
            'form' : CommentCreateForm(),
            'membership' : membership,
            'page_comments' : page_comments,
            'title' : 'Event Chat'
        }
        return render(request, 'events/chat.html', context=context)


@login_required
def comment_delete(request, event_id, comment_id):
    event, membership, is_valid = event_auth_checkpoint(event_id=event_id, request=request)
    if is_valid == False:
        return redirect('general-home')
    comment = get_object_or_404(EventComment, pk=comment_id)
    if request.user == comment.author or request.user.is_staff or membership.is_organizer:
        comment.delete()
        messages.success(request, 'Comment deleted!')
        return redirect('events-chat', event_id=event_id)
    else:
        messages.warning(request, 'Access denied.')
        return redirect('events-chat', event_id=event_id)