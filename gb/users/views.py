from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, HttpResponseRedirect, redirect, render

from events.models import Event, EventMembership
from users.email import send_activation_email
from users.forms import LoginForm, UserRegisterForm
from users.models import User


class LoginView(auth_views.LoginView):
    form_class = LoginForm
    template_name = 'users/login.html'


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Adding user to sample event.  The ID below needs to change if anything ever happens to the object.
            event = Event.objects.get(id='abbb8e18-1a45-42bc-9892-8932358fcbfa')
            membership = EventMembership(user=user, event=event)
            membership.save()
            user.is_active = False
            send_activation_email(user.username, user.email, user.id)
            user.save()

            messages.success(request, f'{user.username} created!  An activation email has been sent to '
                                      f"{user.email}.  Check your spam folder if it isn't in your main inbox.")
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

#test