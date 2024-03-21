from django import forms


class PostForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea(attrs={"rows":"3", "placeholder": 'What are you thinking?'} ),label="", max_length=255)