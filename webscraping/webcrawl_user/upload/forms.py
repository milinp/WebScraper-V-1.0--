from django import forms
from django.forms import ModelForm
from upload.models import UserInput

class DocumentForm(forms.Form):
	docfile = forms.FileField(
		label = 'Select a file',
		help_text = 'max. 42 megabytes'
)

class UserInputForm(ModelForm):
	class Meta:
		model = UserInput