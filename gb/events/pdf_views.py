from django.http import HttpResponse
from django.shortcuts import redirect
from django.template.loader import render_to_string
from weasyprint import HTML

import tempfile

from events.view_utilities import event_auth_checkpoint


def event_order_summary_pdf(request, event_id):
    # Validation
    event, membership, is_valid = event_auth_checkpoint(event_id=event_id, request=request)
    if is_valid == False:
        return redirect('general-home')

    # Render
    context = {

    }
    html_string = render_to_string('bedjango/pdf.html', context=context)
    html = HTML(string=html_string)
    result = html.write_pdf()

    # Response
    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename=event-order-summary.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output = open(output.name, 'r')
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
    html_string = render_to_string('bedjango/pdf.html', context=context)
    html = HTML(string=html_string)
    result = html.write_pdf()

    # Response
    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename=order-breakdown.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output = open(output.name, 'r')
        response.write(output.read())

    return response


def my_order_pdf(request, event_id):
    # Validation
    event, membership, is_valid = event_auth_checkpoint(event_id=event_id, request=request)
    if is_valid == False:
        return redirect('general-home')

    # Render
    context = {

    }
    html_string = render_to_string('bedjango/pdf.html', context=context)
    html = HTML(string=html_string)
    result = html.write_pdf()

    # Response
    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename=event-order-summary.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output = open(output.name, 'r')
        response.write(output.read())

    return response