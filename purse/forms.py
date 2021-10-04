from django import forms
from purse.models import PurseModel


class AddMoneyForm(forms.ModelForm):
    class Meta:
        model = PurseModel
        fields = ['user_id', 'money']

    def __init__(self, *args, **kwargs):
        super(AddMoneyForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    def validate_unique(self):
        pass

