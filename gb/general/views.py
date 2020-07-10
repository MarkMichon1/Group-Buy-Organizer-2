from django.contrib import messages
from django.shortcuts import HttpResponseRedirect, render

from general.models import Instance
from general.utilities import app_db_initialization

def home(request):
    context = {
        'title_h1_override' : True
    }

    return render(request, 'general/home.html', context=context)


def about(request):
    context = {
        'title' : 'About'
    }

    return render(request, 'general/about.html', context=context)


def updates(request): #todo can turn into CBV-listview
    context = {
        'title' : 'Site Updates'
    }

    return render(request, 'general/updates.html', context=context)


def donate(request):
    context = {
        'title': 'Donate'
    }
    return render(request, 'general/donate.html', context=context)


def secret_service_initialization(request):
    instance = Instance.objects.filter(pk=1)
    if instance:
        messages.info(request, 'Already initialized!')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else:
        app_db_initialization()
        instance = Instance(service_initialized=True)
        instance.save()
        messages.success(request, 'Initialized!')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))