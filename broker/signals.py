from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from account.models import Account
from .models import Customer, Trade
from django.utils import timezone

#create customer
@receiver(post_save, sender=Account)
def create_customer(sender, instance, created, **kwargs):
    if created:
        Customer.objects.create(user=instance)

#update customer
@receiver(post_save, sender=Account)
def save_customer(sender, instance, created, **kwargs):
    instance.customer.save()

#set initial profit
@receiver(pre_save, sender=Trade)
def initial_profit(sender, instance, **kwargs):
    if not instance.profit:
        instance.increase = instance.amount
    elif instance.profit:
        instance.increase = instance.profit
