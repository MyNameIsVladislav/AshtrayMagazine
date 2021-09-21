from django import forms
from orderapp.models import Order


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['user', 'first_name', 'last_name', 'email', 'address', 'postal_code', 'city']

    def __init__(self, *args, **kwargs):
        super(OrderCreateForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name == 'user':
                field.widget = forms.HiddenInput()
            field.widget.attrs['class'] = 'form-control'
