from django import forms
from .models import Comment

class commentForm(forms.ModelForm):
    body = forms.CharField(widget=forms.Textarea(attrs={'class': 'textarea', 'placeholder': 'Add comments here....'}), required=True)
    
    class Meta:
        model = Comment
        fields = ('body',)
        