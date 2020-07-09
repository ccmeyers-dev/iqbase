from django.db import models
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string
from django.core.validators import RegexValidator
from django.db.models import Sum
from django.utils import timezone
from django_resized import ResizedImageField

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
    #phone_regex
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}', message="Phone number must be entered in international format ie '+1234567890'.")

    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    unique_id = models.CharField(max_length=10, default=ID, editable=False)
    country = models.CharField(max_length=30, null=True)
    city = models.CharField(max_length=30, null=True)
    address = models.TextField(blank=True, null=True)
    phone_number = models.CharField(validators=[phone_regex], max_length=17, null=True)
    date_of_birth = models.DateField(null=True)
    gender = models.CharField(null=True, max_length=10, choices=GENDER)
    id_front = ResizedImageField(size=[300, 450], upload_to='front_id', null=True)
    id_back = ResizedImageField(size=[300, 450], upload_to='back_id', null=True)

    def __str__(self):
        return str(self.user)

    @property
    def trade(self):
        return Trade.objects.filter(customer=self).aggregate(Sum('amount'))['amount__sum'] or 0
    @property
    def profit(self):
        return Trade.objects.filter(customer=self).aggregate(Sum('profit'))['profit__sum'] or 0
    @property
    def deposit(self):
        return Deposit.objects.filter(customer=self, status='Confirmed').aggregate(Sum('amount'))['amount__sum'] or 0
    @property
    def balance(self):
        return self.deposit - self.trade + self.profit

#wallet
class Wallet(models.Model):
    coin = models.CharField(max_length=20)
    address = models.CharField(max_length=60, default='Coming Soon')

    def __str__(self):
        return self.coin


#trade
STATUS = (
    ('Pending', 'Pending'),
    ('Confirmed', 'Confirmed'),
    ('Cancelled', 'Cancelled'),
)
class Trade(models.Model):
    customer = models.ForeignKey(Customer, null=True, on_delete=models.CASCADE)
    wallet = models.ForeignKey(Wallet, null=True, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    profit = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    duration = models.IntegerField()
    note = models.TextField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.amount) + " - Trade"

#deposit
class Deposit(models.Model):
    customer = models.ForeignKey(Customer, null=True, on_delete=models.CASCADE)
    wallet = models.ForeignKey(Wallet, null=True, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS, default='Pending')
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    note = models.TextField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.amount) + " - Deposit"