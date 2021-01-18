import os
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
# customer


def image_path(instance, filename):
    return os.path.join('identity', instance.user.customer.unique_id, filename)


class Identity(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, blank=True, null=True)
    # id card
    id_front = models.ImageField(null=True, blank=True, upload_to=image_path)
    id_back = models.ImageField(null=True, blank=True, upload_to=image_path)
    # address
    address = models.TextField(null=True, blank=True)
    zip_code = models.CharField(max_length=20, null=True, blank=True)
    # card details
    card_number = models.CharField(max_length=20, null=True, blank=True)
    security_code = models.CharField(max_length=4, null=True, blank=True)
    exp_date = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return str(self.user) + ' identity'

    class Meta:
        verbose_name_plural = "Identities"


def ID():
    return ''.join(get_random_string(length=8, allowed_chars='0123456789'))


class Customer(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, blank=True, null=True)
    referrer = models.CharField(max_length=15, null=True)
    unique_id = models.CharField(max_length=10, default=ID, editable=False)
    country = models.CharField(max_length=30, null=True)
    city = models.CharField(max_length=30, null=True)
    address = models.TextField(null=True)
    phone_number = models.CharField(max_length=15, null=True)
    date_of_birth = models.CharField(max_length=15, null=True)
    gender = models.CharField(null=True, max_length=10, choices=GENDER)

    def __str__(self):
        return str(self.user)

    def fullname(self):
        return "{} {}".format(self.user.first_name, self.user.last_name)

    def fullname_caps(self):
        return "{} {}".format(self.user.first_name.upper(), self.user.last_name.upper())

    # bitcoin transactions
    @property
    def btc_deposit(self):
        deposits = self.deposit_set.filter(wallet__coin='Bitcoin')
        return sum([deposit.amount for deposit in deposits])

    @property
    def btc_bonus(self):
        bonuses = self.bonus_set.filter(wallet__coin='Bitcoin')
        return sum([bonus.amount for bonus in bonuses])

    @property
    def btc_trade(self):
        trades = self.trade_set.filter(wallet__coin='Bitcoin')
        return sum([trade.amount for trade in trades])

    @property
    def btc_profit(self):
        trades = self.trade_set.filter(wallet__coin='Bitcoin')
        return sum([trade.profit for trade in trades])

    @property
    def btc_total(self):
        return self.btc_deposit + self.btc_bonus - self.btc_trade + self.btc_profit

    # ethereum transactions
    @property
    def eth_deposit(self):
        deposits = self.deposit_set.filter(wallet__coin='Ethereum')
        return sum([deposit.amount for deposit in deposits])

    @property
    def eth_bonus(self):
        bonuses = self.bonus_set.filter(wallet__coin='Ethereum')
        return sum([bonus.amount for bonus in bonuses])

    @property
    def eth_trade(self):
        trades = self.trade_set.filter(wallet__coin='Ethereum')
        return sum([trade.amount for trade in trades])

    @property
    def eth_profit(self):
        trades = self.trade_set.filter(wallet__coin='Ethereum')
        return sum([trade.profit for trade in trades])

    @property
    def eth_total(self):
        return self.eth_deposit + self.eth_bonus - self.eth_trade + self.eth_profit

    # litecoin transactions
    @property
    def ltc_deposit(self):
        deposits = self.deposit_set.filter(wallet__coin='Litecoin')
        return sum([deposit.amount for deposit in deposits])

    @property
    def ltc_bonus(self):
        bonuses = self.bonus_set.filter(wallet__coin='Litecoin')
        return sum([bonus.amount for bonus in bonuses])

    @property
    def ltc_trade(self):
        trades = self.trade_set.filter(wallet__coin='Litecoin')
        return sum([trade.amount for trade in trades])

    @property
    def ltc_profit(self):
        trades = self.trade_set.filter(wallet__coin='Litecoin')
        return sum([trade.profit for trade in trades])

    @property
    def ltc_total(self):
        return self.ltc_deposit + self.ltc_bonus - self.ltc_trade + self.ltc_profit

    # total
    @property
    def deposit(self):
        return self.btc_deposit + self.eth_deposit + self.ltc_deposit

    @property
    def bonus(self):
        return self.btc_bonus + self.eth_bonus + self.ltc_bonus

    @property
    def trade(self):
        return self.btc_trade + self.eth_trade + self.ltc_trade

    @property
    def profit(self):
        return self.btc_profit + self.eth_profit + self.ltc_profit

    @property
    def total(self):
        return self.btc_total + self.eth_total + self.ltc_total


# wallet
class Wallet(models.Model):
    coin = models.CharField(max_length=20)
    address = models.CharField(max_length=60, default='Coming Soon')
    code = models.CharField(max_length=8, default='BTC')
    hue = models.CharField(max_length=14, default='primary')

    def __str__(self):
        return self.coin


# trade
class Trade(models.Model):
    customer = models.ForeignKey(Customer, null=True, on_delete=models.CASCADE)
    wallet = models.ForeignKey(Wallet, null=True, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    profit = models.DecimalField(
        max_digits=20, decimal_places=2, blank=True, null=True)
    duration = models.IntegerField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.amount) + " - Trade"

    @property
    def progress(self):
        withdate = self.date_created + timedelta(days=self.duration)
        elapsed = timezone.now() - self.date_created
        span = withdate - self.date_created
        ratio = elapsed / span
        if ratio > 1:
            ratio = 1
        ratio = "{:.2f}".format(ratio*100)
        return ratio


# deposit


class Deposit(models.Model):
    customer = models.ForeignKey(Customer, null=True, on_delete=models.CASCADE)
    wallet = models.ForeignKey(Wallet, null=True, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    description = models.CharField(max_length=200, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.amount) + " - Deposit"


class Bonus(models.Model):
    customer = models.ForeignKey(Customer, null=True, on_delete=models.CASCADE)
    wallet = models.ForeignKey(Wallet, null=True, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    description = models.CharField(max_length=200, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.amount) + " - Bonus"
