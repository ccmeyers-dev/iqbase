from django.contrib import admin
from .models import *
# Register your models here.

class TradeAdmin(admin.ModelAdmin):
    list_filter = ('customer', 'wallet',)

class DepositAdmin(admin.ModelAdmin):
    list_filter = ('customer', 'wallet', 'status')

admin.site.register(Customer)
admin.site.register(Wallet)
admin.site.register(Trade, TradeAdmin)
admin.site.register(Deposit, DepositAdmin)