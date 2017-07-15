from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from .models import Room

class UserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = (
            "email",
            "username",
            "password1",
            "password2"
        )


class RoomForm(forms.ModelForm):
	class Meta:
		model = Room
		fields = ['label']
		
	def clean(self):
		# Super the clean method to maintain main validation and error messages
		super().clean()
		
		try:
			label = self.cleaned_data.get('label')
			room = Room.objects.get(label=label)
			
			raise forms.ValidationError(
				'Room {} already exists'.format(label),
				code='roomexists'
			)
			
		except Room.DoesNotExist:
			return self.cleaned_data