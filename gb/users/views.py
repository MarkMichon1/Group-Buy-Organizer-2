from django.contrib import messages
from django.shortcuts import HttpResponseRedirect, redirect, render

# Create your views here.
def toggle_night_mode(request):
    request.user.toggle_night_mode()
    if request.user.night_mode_enabled:
        messages.info(request, 'Night mode enabled!')
    else:
        messages.info(request, 'Night mode disabled!')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))