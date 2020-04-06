from django import forms

from .models import Message

class MessageFrom(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['text']
        labels = {'text': ''}