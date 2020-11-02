from django.contrib import admin
from .models import *
# Register your models here.


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_name', 'country', 'gender', 'referrer')
    list_filter = ('country', 'referrer', 'gender')
    search_fields = ('user', 'country')

    def get_name(self, obj):
        return '%s %s' % (obj.user.first_name, obj.user.last_name)
    get_name.admin_order_field = 'user'
    get_name.short_description = 'Full Name'


class WalletAdmin(admin.ModelAdmin):
    list_display = ('coin', 'address', 'hue')


class TradeAdmin(admin.ModelAdmin):
    list_display = ('amount', 'customer', 'wallet',
                    'profit', 'duration', 'withdrawal_date')
    list_filter = ('wallet', 'customer',)
    search_fields = ('customer', 'wallet',)


class DepositAdmin(admin.ModelAdmin):
    list_display = ('amount', 'customer', 'wallet')
    list_filter = ('wallet', 'customer',)
    search_fields = ('customer', 'wallet')


class IdentityAdmin(admin.ModelAdmin):
    list_display = ('user', 'card_number')
    search_fields = ('user',)


admin.site.register(Customer, CustomerAdmin)
admin.site.register(Wallet, WalletAdmin)
admin.site.register(Trade, TradeAdmin)
admin.site.register(Deposit, DepositAdmin)
admin.site.register(Identity, IdentityAdmin)
