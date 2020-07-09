from django import forms
from .models import Trade, Deposit, Customer
from broker.models import Wallet

class WalletForm(forms.ModelForm):
    class Meta:
        model = Wallet
        fields = '__all__'
        widgets = {'coin': forms.HiddenInput(),}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['address'].widget.attrs.update({'class': 'form-control'})


class depocorrectform(forms.ModelForm):
    class Meta:
        model = Deposit
        fields = '__all__'
        widgets = {
            'customer': forms.HiddenInput(),
            'status': forms.HiddenInput(),
            'wallet': forms.HiddenInput(),
            'note': forms.HiddenInput(),
            'date_created': forms.HiddenInput()
            }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['amount'].widget.attrs.update({'class': 'form-control'})


class quickfundform(forms.ModelForm):
    class Meta:
        model = Trade
        fields = '__all__'
        widgets = {
            'customer': forms.HiddenInput(),
            'amount': forms.HiddenInput(),
            'wallet': forms.HiddenInput(),
            'duration': forms.HiddenInput(),
            'note': forms.HiddenInput()
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
        self.fields['note'].widget.attrs.update({'class': 'form-control', 'rows':"2"})


class coinform(forms.ModelForm):
    class Meta:
        model = Trade
        fields = '__all__'
        widgets = {'customer': forms.HiddenInput(), 'profit': forms.HiddenInput(), 'wallet': forms.HiddenInput()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['wallet'].widget.attrs.update({'class': 'form-control'})
        self.fields['amount'].widget.attrs.update({'class': 'form-control'})
        self.fields['duration'].widget.attrs.update({'class': 'form-control'})
        self.fields['note'].widget.attrs.update({'class': 'form-control', 'rows':"2"})


class coindepoform(forms.ModelForm):
    class Meta:
        model = Deposit
        fields = '__all__'
        widgets = {'customer': forms.HiddenInput(), 'status': forms.HiddenInput(), 'wallet': forms.HiddenInput()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['wallet'].widget.attrs.update({'class': 'form-control'})
        self.fields['amount'].widget.attrs.update({'class': 'form-control'})
        self.fields['note'].widget.attrs.update({'class': 'form-control', 'rows':"2"})

class tradeform(forms.ModelForm):
    class Meta:
        model = Trade
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['wallet'].widget.attrs.update({'class': 'form-control'})
        self.fields['amount'].widget.attrs.update({'class': 'form-control'})
        self.fields['customer'].widget.attrs.update({'class': 'form-control'})
        self.fields['note'].widget.attrs.update({'class': 'form-control', 'rows':"2"})
        self.fields['profit'].widget.attrs.update({'class': 'form-control'})
        self.fields['duration'].widget.attrs.update({'class': 'form-control'})
        self.fields['date_created'].widget.attrs.update({'class': 'form-control'})

class depositform(forms.ModelForm):
    class Meta:
        model = Deposit
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['wallet'].widget.attrs.update({'class': 'form-control'})
        self.fields['amount'].widget.attrs.update({'class': 'form-control'})
        self.fields['customer'].widget.attrs.update({'class': 'form-control'})
        self.fields['note'].widget.attrs.update({'class': 'form-control', 'rows':"2"})
        self.fields['status'].widget.attrs.update({'class': 'form-control'})
        self.fields['date_created'].widget.attrs.update({'class': 'form-control'})