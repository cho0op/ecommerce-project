from django import forms
from django.contrib.auth import get_user_model

User=get_user_model()

class ContactForm(forms.Form):
    fullname = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class":"form-control",
                "placeholder":"Name",
            }
        )
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "Email",
            }
        )
    )
    content=forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class":"form-control",
                "placeholder":"message",
            }
        )
    )
    def clean_email(self):
        email=self.cleaned_data.get('email')
        if not ".com" in email:
            raise forms.ValidationError("only .com emails")
        return email

    # tested several mistakes in jquery
    # def clean_fullname(self):
    #     name = self.cleaned_data.get("fullname")
    #     if not name[0].isupper():
    #         raise forms.ValidationError("Name has to start form Upper letter")
    #     return name

















