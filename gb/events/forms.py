from django import forms

from datetime import datetime

from events.models import Item, ItemYoutubeVideo


class EventCreateForm(forms.Form):
    current_year = datetime.now().year
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': f'Big Fireworks Spring '
                                                                                        f'{current_year} Group Buy'}))
    description = forms.CharField(required= False, widget=forms.TextInput(attrs={'placeholder': f'Looking forward to '
                                                       f'another fun year!  Deadline for orders: 5/31/{current_year}'}))

class CommentCreateForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea(attrs={'placeholder' : 'Your comment here...'}))


class AddUserForm(forms.Form):
    username = forms.CharField(label='Username To Add To Event:', widget=forms.TextInput(attrs={'placeholder': 'Add username here...'}))


class CreateItemForm(forms.ModelForm):

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


class CaseBuyForm(forms.Form):
    quantity = forms.ChoiceField()


class CreateCaseSplitForm(forms.Form):
    piece_quantity = forms.ChoiceField()