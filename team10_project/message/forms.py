from django import forms

from .models import Messages
from onlinestore.models import Item

class ComposeForm(forms.ModelForm):

    class Meta:
        model = Messages
        fields = ('item', 'receiver', 'msg',)
        labels = {
            'msg': ('Message'),
        }

    def __init__(self, *args, **kwargs):
        super(ComposeForm, self).__init__(*args, **kwargs)

        # related items for the messages can only be approved items
        self.fields['item'].queryset = Item.objects.filter(approved=True)
