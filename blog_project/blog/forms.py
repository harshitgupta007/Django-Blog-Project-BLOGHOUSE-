from django import forms
from blog.models import Comment
from blog.models import Post
class EmailSendForm(forms.Form):
    name=forms.CharField()
    email=forms.EmailField()
    to=forms.EmailField()
    comments=forms.CharField(required=False,widget=forms.Textarea)
class CommentForm(forms.ModelForm):
     class Meta:
            model=Comment
            fields=('name','email','body')

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'title',
            'body',
            'tags',
        ]
