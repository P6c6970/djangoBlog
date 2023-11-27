from django import forms

from blog.models import Comment, Article


class CommentForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['comment_area'].widget.attrs.update({'class': "form-control", "rows": "4"})

    parent_comment = forms.IntegerField(widget=forms.HiddenInput, required=False)
    comment_area = forms.CharField(label="", widget=forms.Textarea)


class ComplaintForm(forms.Form):
    CHOICES = (
        ('1', 'Спам'),
        ('2', 'Запрещенный контент'),
        ('3', 'Обман'),
        ('4', 'Насилие и вражда'),
    )
    type_complaint = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=CHOICES,
    )


class ArticleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        """
        Обновление стилей формы под Bootstrap
        """
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
        self.fields['short_description'].widget.attrs.update({'style': 'height: 150px'})

        self.fields['content'].widget.attrs.update({'class': 'form-control django_ckeditor_5'})
        self.fields['tags'].required = False

    class Meta:
        model = Article
        fields = ('title', 'slug', 'short_description', 'content', 'tags')
