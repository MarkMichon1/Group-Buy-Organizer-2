from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.template.loader import render_to_string
from weasyprint import HTML

import tempfile

from events.view_utilities import event_auth_checkpoint
from users.models import User


def event_order_summary_pdf(request, event_id):
    # Validation
    event, membership, is_valid = event_auth_checkpoint(event_id=event_id, request=request)
    if is_valid == False:
        return redirect('general-home')

    # Render
    context = {

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
    event, membership, is_valid = event_auth_checkpoint(event_id=event_id, request=request)
    if is_valid == False:
        return redirect('general-home')

    # Render
    context = {

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
    user = get_object_or_404(User, pk=user_id)

    # Render
    context = {
        'event': event,
        'title': f"{user.username}'s Order",
        'user': user
    }
    html_string = render_to_string('events/my_order_pdf.html', context=context)
    html = HTML(string=html_string)
    result = html.write_pdf()

    # Response
    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = f"attachment; filename={user.username}'s_Order.pdf"
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output = open(output.name, 'rb')
        response.write(output.read())

    return response