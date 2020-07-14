from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, HttpResponseRedirect, redirect, render

from events.models import Event, EventMembership
from users.forms import UserRegisterForm
from users.models import User


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Adding user to sample event.
            event = Event.objects.get(id='0c4de13a5e37410b86a41fc82eac3d44')
            membership = EventMembership(user=user, event=event)
            membership.save()
            user.is_active = False
            user.save()

            username = user.username
            messages.success(request, f'{username} created!  An activation email has been sent to '
                                      f"{user.email}.")
            return redirect('general-home')
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


@login_required
def toggle_explanations(request):
    request.user.toggle_explanations()
    if request.user.display_explanations:
        messages.info(request, 'How-to explanations enabled!')
    else:
        messages.info(request, 'How-to explanations disabled!')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

#todo integrate captchas into registration


def activate_account(request, pk):
    print(f'pk": {pk}')
    account = get_object_or_404(User, pk=pk)
    if account.is_active:
        messages.success(request, 'Your account is already activated!')
        return redirect('general-home')
    else:
        account.is_active = True
        account.save()
        messages.success(request, 'Account activated!  You may now log in.')
        return redirect('login')