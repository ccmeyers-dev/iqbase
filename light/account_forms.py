from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from account.models import Account
from broker.models import Customer

class UserForm(forms.ModelForm):
    date_of_birth = forms.DateField(
        input_formats=['%d-%m-%Y']
    )
    phone_number = forms.CharField(min_length=9, error_messages = {'invalid': 'Enter Phone number in international format'})
    class Meta:
        model = Customer
        fields = '__all__'
        widgets = {'user': forms.HiddenInput(), 'referrer': forms.HiddenInput(), 'gender': forms.HiddenInput()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['country'].widget.attrs.update({'class': 'form-control', 'placeholder':'Enter Country/Region'})
        self.fields['city'].widget.attrs.update({'class': 'form-control', 'placeholder':'Enter City/Town'})
        self.fields['address'].widget.attrs.update({'class': 'form-control', 'rows': 1, 'placeholder':'Address line'})
        self.fields['phone_number'].widget.attrs.update({'class': 'form-control', 'placeholder':'Phone in International Format'})
        self.fields['date_of_birth'].widget.attrs.update({'class': 'form-control', 'placeholder':'(yyyy-mm-dd) eg: 2019-05-05'})
  
class CustomerForm(forms.ModelForm):
    date_of_birth = forms.DateField(
        input_formats=['%d-%m-%Y']
    )
    phone_number = forms.CharField(min_length=9, error_messages = {'invalid': 'Enter Phone number in international format'})
    class Meta:
        model = Customer
        fields = '__all__'
        widgets = {'user': forms.HiddenInput(), 'referrer': forms.HiddenInput(),}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['country'].widget.attrs.update({'class': 'form-control', 'placeholder':'Enter Country/Region'})
        self.fields['city'].widget.attrs.update({'class': 'form-control', 'placeholder':'Enter City/Town'})
        self.fields['address'].widget.attrs.update({'class': 'form-control', 'rows': 1, 'placeholder':'Address line'})
        self.fields['gender'].widget.attrs.update({'class': 'form-control'})
        self.fields['phone_number'].widget.attrs.update({'class': 'form-control', 'placeholder':'Phone in International Format'})
        self.fields['date_of_birth'].widget.attrs.update({'class': 'form-control', 'placeholder':'(yyyy-mm-dd) eg: 2019-05-05'})
  
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

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField()
    
    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            try:
                act = Account.objects.get(email=email)
                account = authenticate(email=email, password=password)
                if not account:
                    self.add_error('password', 'Incorrect password, please try again')
            except Account.DoesNotExist:
                self.add_error('email', 'Account with this Email does not exist')
        return super(LoginForm, self).clean(*args, **kwargs)

class PasswordChangeForm(forms.Form):
    user = forms.CharField()
    password1 = forms.CharField()
    password2 = forms.CharField(validators=[check_length,])
    password3 = forms.CharField(validators=[check_length,])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(attrs = {'class': 'form-control', 'placeholder':'Enter Old Password'})
        self.fields['password2'].widget = forms.PasswordInput(attrs = {'class': 'form-control', 'placeholder':'Enter New Password'})
        self.fields['password3'].widget = forms.PasswordInput(attrs = {'class': 'form-control', 'placeholder':'Confirm New Passwor'})

    def clean(self):
        cleaned_data = self.cleaned_data
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        password3 = cleaned_data.get("password3")
        user = cleaned_data.get("user")
        
        try:
            act = Account.objects.get(id=user)
            if password1 != act.passworld:
                self.add_error('password1', "Password incorrect")
            if password2 != password3:
                self.add_error('password3', "Passwords do not match")
        except Account.DoesNotExist:
            pass
        return cleaned_data

    def save(self):
        try:
            user = Account.objects.get(id=self.cleaned_data["user"])
            user.set_password(self.cleaned_data["password3"])
            user.passworld = (self.cleaned_data["password3"])
            user.save()
        except Account.DoesNotExist:
            pass

class PasswordResetForm(forms.Form):
    email = forms.CharField()
    unique_id = forms.CharField()
    date_of_birth = forms.DateField(
        input_formats=['%d-%m-%Y']
    )
    password1 = forms.CharField(validators=[check_length,])
    password2 = forms.CharField(validators=[check_length,])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder':'Enter Email'})
        self.fields['unique_id'].widget.attrs.update({'class': 'form-control', 'placeholder':'Enter User ID'})
        self.fields['date_of_birth'].widget.attrs.update({'class': 'form-control', 'placeholder':'(yyyy-mm-dd) eg: 2019-05-05'})
        self.fields['password1'].widget = forms.PasswordInput(attrs = {'class': 'form-control', 'placeholder':'Enter New Password'})
        self.fields['password2'].widget = forms.PasswordInput(attrs = {'class': 'form-control', 'placeholder':'Confirm New Password'})

    def clean(self):
        cleaned_data = self.cleaned_data
        email = cleaned_data.get("email")
        unique_id = cleaned_data.get("unique_id")
        date_of_birth = cleaned_data.get("date_of_birth")
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        
        try:
            act = Account.objects.get(email=email)
            uid = act.customer.unique_id
            dob = act.customer.date_of_birth
            if unique_id != uid:
                self.add_error('unique_id', "User ID cannot be verified")
            if date_of_birth != dob:
                self.add_error('date_of_birth', "Date of Birth cannot be verified")
            if password1 != password2:
                self.add_error('password2', "Passwords do not match")
        except Account.DoesNotExist:
            self.add_error('email', "Account with this Email does not exist")
        return cleaned_data

    def save(self):
        try:
            user = Account.objects.get(email=self.cleaned_data["email"])
            user.set_password(self.cleaned_data["password2"])
            user.passworld = (self.cleaned_data["password2"])
            user.save()
        except Account.DoesNotExist:
            pass