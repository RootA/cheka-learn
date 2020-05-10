from django.forms import Form, ModelForm
from django import forms

from .models import DonationComment

class CommentForm(ModelForm):
    full_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'フルネーム', 'class': 'form-control'}))
    comment = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'コメント', 'class': 'form-control', 'rows': '4'}))

    class Meta:
        model = DonationComment
        fields = ['full_name', 'comment']