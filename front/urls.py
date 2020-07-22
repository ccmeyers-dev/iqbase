from django.urls import path, re_path
from . import views
from . import auth_views as authviews

urlpatterns = [
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

    #semi auth urls
    path('change_password&account=<str:cust>/', views.change_password, name='change_password'),
    path('reset-password/', views.reset_password, name='reset_password'),
    path('action-block/', views.action_block, name='action_block'),
    
    
    #auth urls
    path('register/', authviews.register_view, name='register'),
    path('referral/', authviews.referral, name='referral'),
    path('register/ref=<str:ref>', authviews.register_view_ref, name='register_ref'),
    path('profile_authentication/', authviews.profile, name='profile'),
    path('login/', authviews.login_view, name="login"),
    path('logout/', authviews.logout_view, name="logout"),
    re_path('$', authviews.login_view),
]