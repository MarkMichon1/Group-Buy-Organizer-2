from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import get_object_or_404, HttpResponseRedirect, redirect, render
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from events.forms import EventCommentCreateForm, EventCreateForm
from events.models import Event, EventComment, EventMembership
from events.utilities import event_auth_checkpoint

@login_required
def create_event(request):
    if request.method == 'POST':
        form = EventCreateForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['name']
            description = form.cleaned_data['description']
            event = Event(name=title, description=description, created_by=request.user)
            event.save()
            membership = EventMembership(user=request.user, event=event, is_organizer=True,
                                         is_staff=request.user.is_staff)
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
def event(request, event_pk):
    # Note- until I find a proper way to deal with this, these three lines will be in all event views requiring auth.
    event, membership, is_valid = event_auth_checkpoint(event_pk=event_pk, request=request)
    if is_valid == False:
        return redirect('general-home')

    context = {'title' : event.name,
               'event' : event,
               'membership' : membership}
    return render(request, 'events/event.html', context=context)


@login_required
def edit_event(request):
    context = {} #todo- routes for adding/removing users as well as administrative stuff
    return render(request, 'events/edit_event.html', context=context)


@login_required
def delete_event(request):
    pass


@login_required
def item(request):
    context = {}
    return render(request, 'events/item.html', context=context)


@login_required
def edit_item(request):
    pass


@login_required
def delete_item(request):
    pass


@login_required
def case_split(request):
    context = {}
    return render(request, 'events/case_split.html', context=context)


@login_required
def manage_payments(request):
    context = {}
    return render(request, 'events/manage_payments.html', context=context)


@login_required
def summary(request):
    context = {}
    return render(request, 'events/event_summary.html', context=context)


@login_required
def user_breakdown(request):
    context = {}
    return render(request, 'events/user breakdown.html', context=context)


@login_required
def my_order(request):
    context = {}
    return render(request, 'events/my_order.html', context=context)


@login_required
def chat(request, event_pk):
    event, membership, is_valid = event_auth_checkpoint(event_pk=event_pk, request=request)
    if is_valid == False:
        return redirect('general-home')

    if request.method == 'POST':
        form = EventCommentCreateForm(request.POST)
        if form.is_valid():
            comment = form.cleaned_data['comment']
            event_comment = EventComment(author=request.user, event=event, comment=comment)
            event_comment.save()
            messages.success(request, 'Comment posted!')
            return redirect('general-home') #todo to that event chat
    else:

        event_comments = EventComment.objects.all()
        paginator = Paginator(event_comments, 5)
        page_number = request.GET.get('page')
        page_comments = paginator.get_page(page_number)

        context = {
                   'page_comments': page_comments,
                   'form' : EventCreateForm()
                   }
        return render(request, 'events/chat.html', context=context)

class EventCommentListView(ListView):
    model = EventComment
    template_name = 'events/chat.html'
    context_object_name = 'comments'
    extra_context = {
        'title': 'Event Chat'
    }
    ordering = ['-date_added']
    paginate_by = 50