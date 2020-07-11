from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponseRedirect, redirect, render

from events.models import Event, EventMembership
from users.forms import UserRegisterForm


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Adding user to sample event.
            event = Event.objects.get(id='55758f644ac54bdf8beac031b4934c61')
            membership = EventMembership(user=user, event=event)
            membership.save()
            user.is_active = False
            user.save()

            username = user.username
            messages.success(request, f'{username} created!  An activation email has been sent to '
                                      f"{user.email}.")
            return redirect('login')
    else:
        form = UserRegisterForm()
    context = {
        'form': form,
        'title' : 'User Registration'
    }
    return render(request, 'users/register.html', context=context)


@login_required
def toggle_night_mode(request):
    request.user.toggle_night_mode()
    if request.user.night_mode_enabled:
        messages.info(request, 'Night mode enabled!')
    else:
        messages.info(request, 'Night mode disabled!')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

#todo integrate captchas into registration, AND add into sample gb event at trigger