from django import forms

from informations.models import DeliveryInformation, ReturnInformation


class DeliveryInformationForm(forms.ModelForm):
    class Meta:
        model = DeliveryInformation
        fields = ['text', 'price']


class ReturnInformationForm(forms.ModelForm):
    class Meta:
        model = ReturnInformation
        fields = ['text']
