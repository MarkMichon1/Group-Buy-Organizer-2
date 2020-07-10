from django import forms

from datetime import datetime

from events.models import Event


class EventCreateForm(forms.Form):
    current_year = datetime.now().year
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': f'Big Fireworks Spring '
                                                                                        f'{current_year} Group Buy'}))
    description = forms.CharField(required= False, widget=forms.TextInput(attrs={'placeholder': f'Looking forward to '
                                                       f'another fun year!  Deadline for orders: 5/31/{current_year}'}))