from django import forms

from events.models import Event


class EventCreateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = Event
        fields = ['name']