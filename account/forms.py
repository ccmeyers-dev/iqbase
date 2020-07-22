from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from account.models import Account
from broker.models import Customer

def check_length(value):
    if len(value) < 8:
        raise forms.ValidationError("Password must be at least 8 characters to meet our security standards")

class RegistrationForm(forms.ModelForm):
    password1 = forms.CharField()
    passworld = forms.CharField(validators=[check_length,])
    password2 = None

    class Meta:
        model = Account
        fields = ('email','first_name','last_name','referrer','password1','passworld')
        widgets = {'referrer': forms.HiddenInput(),}

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password1 = cleaned_data.get("password1")
        passworld = cleaned_data.get("passworld")
        if password1 != passworld:
            self.add_error('passworld', "Passwords do not match")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user