from django.contrib.auth.decorators import login_required
from django.shortcuts import render



@login_required
def pm_inbox(request):
    return render(request, 'personal_messages/inbox.html')


@login_required
def pm_sentbox(request):
    return render(request, 'personal_messages/sentbox.html')


@login_required
def pm_compose(request):
    return render(request, 'personal_messages/compose.html')


@login_required
def pm_detail(request, pm_id):
    return render(request, 'personal_messages/detail.html')