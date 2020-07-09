from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from events.forms import EventCreateForm
from events.models import Event


@login_required
def events(request):
    context = {}
    return render(request, 'events/events.html', context=context)


@login_required
def create_event(request):
    context = {}
    return render(request, 'events/create_event.html', context=context)


@login_required
def event(request):
    context = {}
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