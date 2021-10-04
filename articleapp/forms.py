from django import forms

from articleapp.models import CommentsModel


class CommentForm(forms.ModelForm):
    class Meta:
        model = CommentsModel
        fields = ('user_id', 'article_id', 'text')

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name in ('user_id', 'article_id'):
                field.widget = forms.HiddenInput()
            field.widget.attrs['class'] = 'form-control'
