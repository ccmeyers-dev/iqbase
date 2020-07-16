from django.contrib import admin
from django.urls import path, include, re_path
from account import views
from broker.views import home

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('ccmeyers100/', admin.site.urls),
    path('', include('front.urls')),
    path('register/', views.register_view, name='register'),
    path('referral/', views.referral, name='referral'),
    path('register/ref=<str:ref>', views.register_view_ref, name='register_ref'),
    path('change_password&account=<str:cust>/', views.change_password, name='change_password'),
    path('reset_password/', views.reset_password, name='reset_password'),
    path('profile_authentication/', views.profile, name='profile'),
    path('action_block/', views.action_block, name='action_block'),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    #re_path('$', home),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
