from django.urls import path
from broker import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('userprofile/', views.userprofile, name='userprofile'),
    path('receipt/', views.receipt, name='receipt'),
    #admin
    path('administrator/', views.administrator, name='administrator'),
    path('user/<str:pk>/', views.user, name='user'),
    #edit
    path('update_trade/<str:pk>/', views.update_trade, name='update_trade'),
    path('delete_trade/<str:pk>/', views.delete_trade, name='delete_trade'),
    path('update_deposit/<str:pk>/', views.update_deposit, name='update_deposit'),
    path('delete_deposit/<str:pk>/', views.delete_deposit, name='delete_deposit'),
    #coin
    path('bitcoin/<str:pk>/', views.bitcoin, name='bitcoin'),
    path('ethereum/<str:pk>/', views.ethereum, name='ethereum'),
    path('litecoin/<str:pk>/', views.litecoin, name='litecoin'),
    #deposit
    path('bitcoindepo/<str:pk>/', views.bitcoindepo, name='bitcoindepo'),
    path('ethereumdepo/<str:pk>/', views.ethereumdepo, name='ethereumdepo'),
    path('litecoindepo/<str:pk>/', views.litecoindepo, name='litecoindepo'),
    #withdrawal
    path('bitcoinwith/<str:pk>/', views.bitcoinwith, name='bitcoinwith'),
    path('ethereumwith/<str:pk>/', views.ethereumwith, name='ethereumwith'),
    path('litecoinwith/<str:pk>/', views.litecoinwith, name='litecoinwith'),
    #auth
    path('del_user/<str:pk>/', views.del_user, name='del_user'),
    path('deactivate/<str:pk>/', views.deactivate, name='deactivate'),
    path('activate/<str:pk>/', views.activate, name='activate'),
]