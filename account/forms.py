from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from .models import Account
from broker.models import Customer

class UserForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['id_front', 'id_back']
        widgets = {'user': forms.HiddenInput(), 'id_front': forms.HiddenInput(), 'id_back': forms.HiddenInput(), 'gender': forms.HiddenInput()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['country'].widget.attrs.update({'class': 'form-control', 'placeholder':'Enter Country/Region'})
        self.fields['city'].widget.attrs.update({'class': 'form-control', 'placeholder':'Enter City/Town'})
        self.fields['address'].widget.attrs.update({'class': 'form-control', 'rows': 1, 'placeholder':'Address line'})
        self.fields['gender'].widget.attrs.update({'class': 'form-control'})
        self.fields['phone_number'].widget.attrs.update({'class': 'form-control', 'placeholder':'Phone in International Format'})
        self.fields['date_of_birth'].widget.attrs.update({'class': 'form-control', 'placeholder':'(yyy-mm-dd)  eg: 2019-05-05 ', 'placeholder':'(yyy-mm-dd)  eg: 2019-05-05 '})
  

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        widgets = {'user': forms.HiddenInput()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['country'].widget.attrs.update({'class': 'form-control', 'placeholder':'Enter Country/Region'})
        self.fields['city'].widget.attrs.update({'class': 'form-control', 'placeholder':'Enter City/Town'})
        self.fields['address'].widget.attrs.update({'class': 'form-control', 'rows': 1, 'placeholder':'Address line'})
        self.fields['gender'].widget.attrs.update({'class': 'form-control'})
        self.fields['phone_number'].widget.attrs.update({'class': 'form-control', 'placeholder':'Phone in International Format'})
        self.fields['date_of_birth'].widget.attrs.update({'class': 'form-control', 'placeholder':'(yyy-mm-dd)  eg: 2019-05-05 ', 'placeholder':'(yyy-mm-dd)  eg: 2019-05-05 '})
  
def check_length(value):
    if len(value) < 8:
        raise forms.ValidationError("Password must be at least 8 characters to meet our security standards")

class RegistrationForm(forms.ModelForm):
    password1 = forms.CharField()
    passworld = forms.CharField(validators=[check_length,])
    password2 = None

    class Meta:
        model = Account
        fields = ('email','first_name','last_name','password1','passworld')

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

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField()
    
    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            account = authenticate(email=email, password=password)
            if not account:
                raise forms.ValidationError('Email or Password Incorrect, try again')
        return super(LoginForm, self).clean(*args, **kwargs)