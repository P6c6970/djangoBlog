from django import forms

from blog.models import Comment


class CommentForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['comment_area'].widget.attrs.update({'class': "form-control", "rows": "4"})

    parent_comment = forms.IntegerField(widget=forms.HiddenInput, required=False)
    comment_area = forms.CharField(label="", widget=forms.Textarea)
