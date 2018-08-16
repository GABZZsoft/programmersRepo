from django import forms
from .models import Topic

class NewTopicForm(forms.ModelForm):
    message = forms.CharField(widget=forms.Textarea(attrs={'rows':5, 'placeholder':'whats up ?'}), max_length=4000, help_text='Max length is 400 char')

    class Meta:
        model= Topic
        fields = ['subject', 'message']
