from django.core.mail import send_mail
from django.template import loader
from django.utils.html import strip_tags

def send_activation_email(username, target_email, activation_uuid):

    html_message = loader.render_to_string('users/activation_email.html', context={
        'activation_uuid': activation_uuid,
        'username': username
    })
    plain_message = strip_tags(html_message)
    send_mail('Pyro Group Buys -- Account Activation Link', plain_message, 'noreply@pyrogroupbuys.com',
              [f'{target_email}'], html_message=html_message, fail_silently=False)