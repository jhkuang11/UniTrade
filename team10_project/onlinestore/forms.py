from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Item
from . import models
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from message.models import Messages

class ItemForm(forms.ModelForm):
	class Meta:
		model = Item
		fields=["title", "price", "description", "category", "image"]
	# def clean_image(self):
	# 	image = self.cleaned_data.get('image', False)
	# 	if image:
	# 		if image._size > 3*1024*1024:
	# 			raise ValidationError("Image file too large ( > 3 mb)")
	# 		return image
	# 	else:
	# 		raise ValidationError("Couldn't read uploaded image")

class ContactForm(forms.ModelForm):

    class Meta:
        model = Messages
        fields = ('item','receiver', 'msg',)
        labels = {
        	'item': (),
        	'receiver': (),
            'msg': (),
        }
        widgets = {
            'msg': forms.Textarea(
                attrs={'placeholder': 'Leave a message',
                		'style': 'width:100%',
                }),
        }
