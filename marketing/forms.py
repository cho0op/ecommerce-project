from django import forms
from .models import MarketingPreference


class MarketingPreferenceForm(forms.ModelForm):
    subscribed = forms.BooleanField(label="Receive marketing emails")

    class Meta:
        model = MarketingPreference
        fields = ['subscribed']
