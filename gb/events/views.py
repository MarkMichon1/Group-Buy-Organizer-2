from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import get_object_or_404, HttpResponseRedirect, redirect, render
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from events.forms import EventCreateForm
from events.models import Event, EventMembership
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
            messages.success(request, f"Event successfully created!  Click the Event Settings button in the organizer"
                                      f"toolbar to add more members.") #todo
            return redirect('general-home')
    else:
        context = {
            'form' : EventCreateForm(),
            'title' : 'New Event'
                   }
        return render(request, 'events/create_event.html', context=context)

@login_required
def event(request, pk):
    event, membership = event_auth_checkpoint(pk, request)

    context = {'title' : event.name}
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
def chat(request):
    #todo - enable/disable chat, delete invididual messages
    context = {}
    return render(request, 'events/chat.html', context=context)