from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponseRedirect, redirect, render

@login_required
def toggle_night_mode(request):
    request.user.toggle_night_mode()
    if request.user.night_mode_enabled:
        messages.info(request, 'Night mode enabled!')
    else:
        messages.info(request, 'Night mode disabled!')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))