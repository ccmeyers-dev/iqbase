from django.urls import path
from broker import views

urlpatterns = [
    #test urls
    path('test/', views.test, name='test'),
    path('invoice/', views.invoice, name='invoice'),

    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.userprofile, name='userprofile'),
    path('receipt/', views.receipt, name='receipt'),
    #admin
    path('administrator/', views.administrator, name='administrator'),
    path('user&target=<str:pk>/', views.user, name='user'),
    #edit
    path('update_trade&target=<str:pk>/', views.update_trade, name='update_trade'),
    path('delete_trade&target=<str:pk>/', views.delete_trade, name='delete_trade'),
    path('update_deposit&target=<str:pk>/', views.update_deposit, name='update_deposit'),
    path('delete_deposit&target=<str:pk>/', views.delete_deposit, name='delete_deposit'),
    #coin
    path('trade&coin=bitcoin&target=<str:pk>/', views.bitcoin, name='bitcoin'),
    path('trade&coin=ethereum&target=<str:pk>/', views.ethereum, name='ethereum'),
    path('trade&coin=litecoin&target=<str:pk>/', views.litecoin, name='litecoin'),
    #deposit
    path('deposit&coin=bitcoin&target=<str:pk>/', views.bitcoindepo, name='bitcoindepo'),
    path('deposit&coin=ethereum&target=<str:pk>/', views.ethereumdepo, name='ethereumdepo'),
    path('deposit&coin=litecoin&target=<str:pk>/', views.litecoindepo, name='litecoindepo'),
    #withdrawal
    path('withdrawal&coin=bitcoin&target=<str:pk>/', views.bitcoinwith, name='bitcoinwith'),
    path('withdrawal&coin=ethereum&target=<str:pk>/', views.ethereumwith, name='ethereumwith'),
    path('withdrawal&coin=litecoin&target=<str:pk>/', views.litecoinwith, name='litecoinwith'),
    #auth
    path('delete_user&target=<str:pk>/', views.del_user, name='del_user'),
    path('toggle_admin&target=<str:pk>/', views.toggle_admin, name='toggle_admin'),
    path('deactivate_user&target=<str:pk>/', views.deactivate, name='deactivate'),
    path('activate_user&target=<str:pk>/', views.activate, name='activate'),
]