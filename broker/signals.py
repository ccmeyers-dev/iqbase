from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from account.models import Account
from .models import Customer, Trade, Deposit
from django.utils import timezone

#create customer
@receiver(post_save, sender=Account)
def create_customer(sender, instance, created, **kwargs):
    if created:
        Customer.objects.create(user=instance, referrer=instance.referrer)

#update customer
@receiver(post_save, sender=Account)
def save_customer(sender, instance, created, **kwargs):
    instance.customer.save()

#referrer bonus
@receiver(pre_save, sender=Trade)
def referrer_bonus(sender, instance, **kwargs):
    trade_count = instance.customer.trade_set.all().count()
    bonus = float(instance.amount) * 0.25
    desc = "Referral bonus - " + str(instance.customer.user.first_name) + " " + str(instance.customer.user.last_name)
    ref = instance.customer.referrer
    if Customer.objects.filter(unique_id=ref).exists():
        referrer = Customer.objects.get(unique_id=ref)
        if trade_count ==  0:
            Deposit.objects.create(customer=referrer, amount=bonus, wallet=instance.wallet, description=desc)
            Deposit.objects.create(customer=instance.customer, amount=bonus, wallet=instance.wallet, description="Referral bonus")

