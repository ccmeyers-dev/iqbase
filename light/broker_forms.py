from django import forms
from broker.models import Trade, Deposit, Customer, Wallet, Identity


class IdentityForm(forms.ModelForm):
    class Meta:
        model = Identity
        fields = '__all__'
        widgets = {'user': forms.HiddenInput()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['address'].widget.attrs.update({'class': 'form-control'})


class WalletForm(forms.ModelForm):
    class Meta:
        model = Wallet
        fields = '__all__'
        widgets = {'coin': forms.HiddenInput(), 'code': forms.HiddenInput(),
                   'hue': forms.HiddenInput()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['address'].widget.attrs.update({'class': 'form-control'})


class depocorrectform(forms.ModelForm):
    class Meta:
        model = Deposit
        fields = '__all__'
        widgets = {
            'customer': forms.HiddenInput(),
            'wallet': forms.HiddenInput(),
            'date_created': forms.HiddenInput()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['amount'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update(
            {'class': 'form-control'})


class quickfundform(forms.ModelForm):
    class Meta:
        model = Trade
        fields = '__all__'
        widgets = {
            'customer': forms.HiddenInput(),
            'amount': forms.HiddenInput(),
            'wallet': forms.HiddenInput(),
            'duration': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['profit'].widget.attrs.update({'class': 'form-control'})


class fundform(forms.ModelForm):
    class Meta:
        model = Trade
        fields = '__all__'
        widgets = {'customer': forms.HiddenInput()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['wallet'].widget.attrs.update({'class': 'form-control'})
        self.fields['amount'].widget.attrs.update({'class': 'form-control'})
        self.fields['profit'].widget.attrs.update({'class': 'form-control'})
        self.fields['duration'].widget.attrs.update({'class': 'form-control'})


class coinform(forms.ModelForm):
    class Meta:
        model = Trade
        fields = '__all__'
        widgets = {'customer': forms.HiddenInput(
        ), 'profit': forms.HiddenInput()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['wallet'].widget.attrs.update(
            {'class': 'form-control', 'hidden': 'hidden'})
        self.fields['amount'].widget.attrs.update({'class': 'form-control'})
        self.fields['duration'].widget.attrs.update({'class': 'form-control'})


class coindepoform(forms.ModelForm):
    class Meta:
        model = Deposit
        fields = '__all__'
        widgets = {'customer': forms.HiddenInput(
        ), 'wallet': forms.HiddenInput()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['description'].widget.attrs.update(
            {'class': 'form-control'})
        self.fields['amount'].widget.attrs.update({'class': 'form-control'})
