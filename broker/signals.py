from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from account.models import Account
from .models import Customer, Bonus, Wallet
from django.utils import timezone

# create customer


@receiver(post_save, sender=Account)
def create_customer(sender, instance, created, **kwargs):
    if created:
        Customer.objects.create(user=instance, referrer=instance.referrer)

# update customer


@receiver(post_save, sender=Account)
def save_customer(sender, instance, created, **kwargs):
    instance.customer.save()

# referrer bonus


@receiver(post_save, sender=Customer)
def referrer_bonus(sender, instance, created, **kwargs):
    if created and instance.referrer:
        bonus = 25
        bitcoin_wallet = Wallet.objects.get(coin='Bitcoin')
        referrer_desc = "Referral bonus - " + \
            str(instance.user.first_name) + \
            " " + str(instance.user.last_name)
        ref = instance.referrer
        if Customer.objects.filter(unique_id=ref).exists():
            referrer = Customer.objects.get(unique_id=ref)
            Bonus.objects.create(customer=referrer, amount=bonus,
                                 wallet=bitcoin_wallet, description=referrer_desc)
            Bonus.objects.create(customer=instance, amount=bonus,
                                 wallet=bitcoin_wallet, description="Referral bonus")
