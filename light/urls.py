from django.urls import path, re_path
from . import views
from . import auth_views as authviews

urlpatterns = [
    # home
    path('about/', views.about, name='about'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('term-condition/', views.term_condition, name='term_condition'),


    # user
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('customer-data/', views.customer_data, name='customer_data'),
    path('trade-view/', views.trade_view, name='trade_view'),
    path('trade&query=all/', views.trade_history, name='trade_history'),
    path('deposit&query=all/', views.deposit_history, name='deposit_history'),
    path('account/', views.account, name='account'),
    path('profile/', views.userprofile, name='userprofile'),
    path('settings&action=name/', views.settings_name, name='settings_name'),
    path('settings&action=profile/',
         views.settings_profile, name='settings_profile'),
    path('settings&action=contact/',
         views.settings_contact, name='settings_contact'),
    path('settings&action=identity/',
         views.settings_identity, name='settings_identity'),


    # admin
    path('administrator/', views.administrator, name='administrator'),
    path('user&target=<str:pk>/', views.user, name='user'),
    path('receipt/', views.receipt, name='receipt'),
    path('delete-user&target=<str:pk>/', views.del_user, name='del_user'),
    path('toggle-admin&target=<str:pk>/',
         views.toggle_admin, name='toggle_admin'),
    path('deactivate-user&target=<str:pk>/',
         views.deactivate, name='deactivate'),
    path('activate-user&target=<str:pk>/', views.activate, name='activate'),
    # reject card details
    path('reject_card/<str:pk>/', views.reject_card, name='reject_card'),
    # edit
    path('update-trade&target=<str:pk>/',
         views.update_trade, name='update_trade'),
    path('delete-trade&target=<str:pk>/',
         views.delete_trade, name='delete_trade'),
    path('update-deposit&target=<str:pk>/',
         views.update_deposit, name='update_deposit'),
    path('delete-deposit&target=<str:pk>/',
         views.delete_deposit, name='delete_deposit'),
    # deposit
    path('deposit&coin=bitcoin&target=<str:pk>/',
         views.bitcoindepo, name='bitcoindepo'),
    path('deposit&coin=ethereum&target=<str:pk>/',
         views.ethereumdepo, name='ethereumdepo'),
    path('deposit&coin=litecoin&target=<str:pk>/',
         views.litecoindepo, name='litecoindepo'),
    # trade
    path('trade&coin=bitcoin&target=<str:pk>/', views.bitcoin, name='bitcoin'),
    path('trade&coin=ethereum&target=<str:pk>/',
         views.ethereum, name='ethereum'),
    path('trade&coin=litecoin&target=<str:pk>/',
         views.litecoin, name='litecoin'),
    # withdrawal
    path('withdrawal&coin=bitcoin&target=<str:pk>/',
         views.bitcoinwith, name='bitcoinwith'),
    path('withdrawal&coin=ethereum&target=<str:pk>/',
         views.ethereumwith, name='ethereumwith'),
    path('withdrawal&coin=litecoin&target=<str:pk>/',
         views.litecoinwith, name='litecoinwith'),


    # semi auth urls
    path('change-password&account=<str:cust>/',
         views.settings_password, name='change_password'),
    path('reset-password/', views.reset_password, name='reset_password'),
    path('action-block/', views.action_block, name='action_block'),


    # auth urls
    path('register/', authviews.register_view, name='register'),
    path('referral/', authviews.referral, name='referral'),
    path('register/ref=<str:ref>', authviews.register_view_ref, name='register_ref'),
    path('profile-authentication/', authviews.profile, name='profile'),
    path('login/', authviews.login_view, name="login"),
    path('logout/', authviews.logout_view, name="logout"),
    # re_path('$', authviews.login_view),
]
