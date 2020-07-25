from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox
from django import forms

from datetime import datetime

from events.models import Event, Item, ItemYoutubeVideo


class EventCreateForm(forms.Form):
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(EventCreateForm, self).__init__(*args, **kwargs)

        if user.night_mode_enabled:
            data_theme = 'dark'
        else:
            data_theme = 'light'

        self.fields['captcha'] = ReCaptchaField(
            widget=ReCaptchaV2Checkbox(
                attrs={
                    'data-theme': f'{data_theme}'
                }
            )
        )

    current_year = datetime.now().year
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': f'Big Fireworks Spring '
                                                                                        f'{current_year} Group Buy'}))
    description = forms.CharField(required= False, widget=forms.TextInput(attrs={'placeholder': f'Looking forward to '
                                                       f'another fun year!  Deadline for orders: 5/31/{current_year}'}))
    captcha = ReCaptchaField()

class CommentCreateForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea(attrs={'placeholder' : 'Your comment here...'}))


class AddUserForm(forms.Form):
    username = forms.CharField(label='Username To Add To Event:', widget=forms.TextInput(attrs={'placeholder': 'Add username here...'}))


class ItemForm(forms.ModelForm):

    class Meta:
        model = Item
        fields = ['category', 'name', 'price', 'packing']
        labels = {
            'name': 'Item Name.  A good format to use is Brand- Item Name',
            'price': 'Case Price:',
            'packing': 'Case Packing.  Type 4 for 4/1, 12 for 12/1, etc.'
        }


class CreateItemYoutubeVideoForm(forms.ModelForm):
    class Meta:
        model = ItemYoutubeVideo
        fields = ['url']
        labels = {
            'url': 'Paste a Youtube video URL here.'
        }


class QuantitySelectForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.max_pieces = kwargs.pop('max_pieces')
        self.item_price = kwargs.pop('item_price')
        self.item_packing = kwargs.pop('item_packing')
        self.whole_cases = kwargs.pop('whole_cases')
        self.initial_qty = kwargs.pop('initial_qty')
        super(QuantitySelectForm, self).__init__(*args, **kwargs)

        def return_qty_price_select_field(self):
            choices_list = []
            if self.whole_cases == False:
                for i in range(self.max_pieces):
                    choices_list.append(
                        (i + 1,
                         f'{i + 1}/{self.item_packing} -- ${round((i + 1) * (self.item_price / self.item_packing), 2)}'))
            else:
                for i in range(self.max_pieces):
                    choices_list.append((i, f'{i} -- ${round(i * self.item_price, 2)}'))
            return choices_list

        self.fields['quantity'] = forms.ChoiceField(choices=return_qty_price_select_field(self), initial=self.initial_qty)

    quantity = forms.ChoiceField()


class EventSettingsForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = ['name', 'description', 'is_locked', 'users_full_event_visibility', 'extra_charges']
        labels = {
            'name': 'Event Name',
            'description': 'Event Description',
            'is_locked': 'Lock Event',
            'users_full_event_visibility': 'Allow users to see all event order data (summary, orders of others)',
            'extra_charges': "Extra charges for event.  Will be distributed proportionately to the size of everyone's order:"
        }
