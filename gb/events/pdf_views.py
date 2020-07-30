from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.template.loader import render_to_string
from weasyprint import HTML

import tempfile

from events.models import EventMembership
from events.view_utilities import event_auth_checkpoint
from users.models import User


def event_order_summary_pdf(request, event_id):
    # Validation
    event, membership, is_valid = event_auth_checkpoint(event_id=event_id, request=request, summary_or_breakdown=True)
    if is_valid == False:
        return redirect('general-home')

    # Render
    summary_data = event.generate_event_pages_contents(page_type='summary')
    context = {
        'is_pdf': True,
        'summary_data': summary_data,
        'title': 'Event Order Summary'
    }
    html_string = render_to_string('events/event_order_summary_pdf.html', context=context)
    html = HTML(string=html_string)
    result = html.write_pdf()

    # Response
    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'attachment; filename=Event_Order_Summary.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output = open(output.name, 'rb')
        response.write(output.read())

    return response


def order_breakdown_pdf(request, event_id):
    # Validation
    event, membership, is_valid = event_auth_checkpoint(event_id=event_id, request=request, summary_or_breakdown=True)
    if is_valid == False:
        return redirect('general-home')

    # Render
    breakdown_data = event.generate_event_pages_contents(page_type='breakdown')
    context = {
        'breakdown_data': breakdown_data,
        'is_pdf': True,
        'title': 'Order Broken Down By Users'
    }
    html_string = render_to_string('events/user_breakdown_pdf.html', context=context)
    html = HTML(string=html_string)
    result = html.write_pdf()

    # Response
    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'attachment; filename=Order_Breakdown.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output = open(output.name, 'rb')
        response.write(output.read())

    return response


def my_order_pdf(request, event_id, user_id):
    # Validation
    event, membership, is_valid = event_auth_checkpoint(event_id=event_id, request=request)
    if is_valid == False:
        return redirect('general-home')
    targetted_user = get_object_or_404(User, pk=user_id)
    if not event.users_full_event_visibility and targetted_user != request.user and not membership.is_organizer:
        messages.info(request, "This view is restricted for organizers only.")
        return redirect('events-event', event_id=event_id)

    # Render
    targetted_membership = EventMembership.objects.filter(event=event).get(user=targetted_user)
    my_order_data = event.generate_event_pages_contents(page_type='my_order', membership=targetted_membership)
    context = {
        'event': event,
        'is_pdf': True,
        'my_order_data': my_order_data,
        'title': f"{targetted_user.username}'s Order",
        'targetted_user': targetted_user
    }
    html_string = render_to_string('events/my_order_pdf.html', context=context)
    html = HTML(string=html_string)
    result = html.write_pdf()

    # Response
    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = f"attachment; filename={targetted_user.username}'s_Order.pdf"
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output = open(output.name, 'rb')
        response.write(output.read())

    return response