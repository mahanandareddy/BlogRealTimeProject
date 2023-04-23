from django import forms
from BlogApp.models import Comment
class EmailSendFrom(forms.Form):
    name = forms.CharField(max_length=50)
    email = forms.EmailField()
    to =forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'mail', 'body')
