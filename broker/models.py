from django.db import models
from django.db.models import Sum, ExpressionWrapper, F, DateTimeField
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string
from django.core.validators import RegexValidator
from django.utils import timezone, formats
from django_resized import ResizedImageField
from datetime import datetime, timedelta
from django.utils import timezone
User = get_user_model()

GENDER = (
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Other', 'Other'),
)
#customer
def ID():
    return ''.join(get_random_string(length=8, allowed_chars='0123456789'))

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    referrer = models.CharField(max_length=15, null=True)
    unique_id = models.CharField(max_length=10, default=ID, editable=False)
    country = models.CharField(max_length=30, null=True)
    city = models.CharField(max_length=30, null=True)
    address = models.TextField(null=True)
    phone_number = models.CharField(max_length=15, null=True)
    date_of_birth = models.DateField(null=True)
    gender = models.CharField(null=True, max_length=10, choices=GENDER)

    def __str__(self):
        return str(self.user)
    
    def fullname(self):
        return "{} {}".format(self.user.first_name, self.user.last_name)
    #bitcoin transactions
    @property
    def btc_trade_amount(self):
        return Trade.objects.filter(customer=self, wallet__coin='Bitcoin').aggregate(Sum('amount'))['amount__sum'] or 0

    @property
    def btc_depo_amount(self):
        return Deposit.objects.filter(customer=self, wallet__coin='Bitcoin').aggregate(Sum('amount'))['amount__sum'] or 0

    @property
    def btc_profit(self):
        return Trade.objects.filter(customer=self, wallet__coin='Bitcoin').aggregate(Sum('profit'))['profit__sum'] or 0

    @property
    def btc_completed(self):
        return Trade.objects.filter(customer=self, wallet__coin='Bitcoin', withdrawal_date__lte=timezone.now()).aggregate(Sum('profit'))['profit__sum'] or 0
    
    @property
    def btc_balance(self):
        return self.btc_depo_amount - self.btc_trade_amount + self.btc_profit
        
    @property
    def btc_available(self):
        return self.btc_depo_amount - self.btc_trade_amount + self.btc_completed

    #ethereum transactions
    @property
    def eth_trade_amount(self):
        return Trade.objects.filter(customer=self, wallet__coin='Ethereum').aggregate(Sum('amount'))['amount__sum'] or 0

    @property
    def eth_depo_amount(self):
        return Deposit.objects.filter(customer=self, wallet__coin='Ethereum').aggregate(Sum('amount'))['amount__sum'] or 0

    @property
    def eth_profit(self):
        return Trade.objects.filter(customer=self, wallet__coin='Ethereum').aggregate(Sum('profit'))['profit__sum'] or 0

    @property
    def eth_completed(self):
        return Trade.objects.filter(customer=self, wallet__coin='Ethereum', withdrawal_date__lte=timezone.now()).aggregate(Sum('profit'))['profit__sum'] or 0
    
    @property
    def eth_balance(self):
        return self.eth_depo_amount - self.eth_trade_amount + self.eth_profit
        
    @property
    def eth_available(self):
        return self.eth_depo_amount - self.eth_trade_amount + self.eth_completed

    #litecoin transactions
    @property
    def ltc_trade_amount(self):
        return Trade.objects.filter(customer=self, wallet__coin='Litecoin').aggregate(Sum('amount'))['amount__sum'] or 0

    @property
    def ltc_depo_amount(self):
        return Deposit.objects.filter(customer=self, wallet__coin='Litecoin').aggregate(Sum('amount'))['amount__sum'] or 0

    @property
    def ltc_profit(self):
        return Trade.objects.filter(customer=self, wallet__coin='Litecoin').aggregate(Sum('profit'))['profit__sum'] or 0

    @property
    def ltc_completed(self):
        return Trade.objects.filter(customer=self, wallet__coin='Litecoin', withdrawal_date__lte=timezone.now()).aggregate(Sum('profit'))['profit__sum'] or 0
    
    @property
    def ltc_balance(self):
        return self.ltc_depo_amount - self.ltc_trade_amount + self.ltc_profit
        
    @property
    def ltc_available(self):
        return self.ltc_depo_amount - self.ltc_trade_amount + self.ltc_completed

    #total
    @property
    def trade_amount(self):
        return self.btc_trade_amount + self.eth_trade_amount + self.ltc_trade_amount

    @property
    def deposit_amount(self):
        return self.btc_depo_amount + self.eth_depo_amount + self.ltc_depo_amount

    @property
    def profit(self):
        return self.btc_profit + self.eth_profit + self.ltc_profit

    @property
    def completed(self):
        return self.btc_completed + self.eth_completed + self.ltc_completed

    @property
    def balance(self):
        return self.btc_balance + self.eth_balance + self.ltc_balance
        
    @property
    def available(self):
        return self.btc_available + self.eth_available + self.ltc_available

    
#wallet
class Wallet(models.Model):
    coin = models.CharField(max_length=20)
    address = models.CharField(max_length=60, default='Coming Soon')
    code = models.CharField(max_length=8, default='BTC')
    hue = models.CharField(max_length=14, default='primary')

    def __str__(self):
        return self.coin


#trade
class Trade(models.Model):
    customer = models.ForeignKey(Customer, null=True, on_delete=models.CASCADE)
    wallet = models.ForeignKey(Wallet, null=True, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    profit = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    duration = models.IntegerField()
    date_created = models.DateTimeField(auto_now_add=True)
    withdrawal_date = models.DateTimeField(editable=False, blank=True, null=True)
    
    def __str__(self):
        return str(self.amount) + " - Trade"

    def save(self, *args, **kwargs):
        span = timedelta(days=self.duration)
        if self.date_created is not None:
            self.withdrawal_date = self.date_created + span
        else:
            self.withdrawal_date = timezone.now() + span
        super(Trade, self).save(*args, **kwargs)

    @property
    def progress(self):
        withdate = self.date_created + timedelta(days=self.duration)
        elapsed = timezone.now() - self.date_created
        span = withdate - self.date_created
        ratio = elapsed / span
        if ratio > 1:
            ratio = 1
        ratio = "{:.2f}%".format(ratio*100)
        return ratio

    @property
    def current(self):
        withdate = self.date_created + timedelta(days=self.duration)
        elapsed = timezone.now() - self.date_created
        span = withdate - self.date_created
        ratio = elapsed / span
        if ratio > 1:
            ratio = 1
        current = ratio * float(self.profit)
        return current

#deposit
class Deposit(models.Model):
    customer = models.ForeignKey(Customer, null=True, on_delete=models.CASCADE)
    wallet = models.ForeignKey(Wallet, null=True, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    description = models.CharField(max_length=200, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.amount) + " - Deposit"