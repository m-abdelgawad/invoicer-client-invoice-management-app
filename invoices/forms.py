from django import forms
from .models import Client, Invoice, Service, Profile


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['first_name', 'last_name', 'company', 'email_address', 'mobile_number', 'city', 'country', 'logo']


class InvoiceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            self.fields['client'].queryset = Client.objects.filter(author=user)

    class Meta:
        model = Invoice
        fields = ['title', 'due_date', 'currency', 'status', 'notes', 'client']


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        exclude = ['id']
        fields = ['title', 'description', 'quantity', 'quantity_unit', 'unit_price', 'total_price', ]


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['author']
        fields = ['first_name', 'last_name', 'company', 'email_address', 'mobile_number', 'city', 'country', 'logo']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'company', 'email_address', 'mobile_number', 'city', 'country', 'logo']
