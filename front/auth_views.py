from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from smtplib import SMTPException
from account.models import Account
from broker.models import Customer
from broker.decorators import *
from .account_forms import *

@login_required(login_url='login')
def profile(request):
    user = request.user
    ref = user.referrer
    if  user.is_setup:
        return redirect('dashboard')
    cust = user.customer
    if request.POST:
        form = CustomerForm(request.POST, instance=cust)
        if form.is_valid():
            user.is_setup = True
            user.save()
            form.save()
            if settings.DEBUG:
                return redirect('dashboard')
            else:
                try:
                    name = user.first_name
                    subject = 'Welcome to ' + settings.SITE_NAME + ' Trade'
                    html_message = render_to_string('front/mail.html', {
                        'name': name,
                        'site': settings.SITE_NAME,
                        'url': settings.SITE_URL
                        })
                    plain_message = strip_tags(html_message)
                    from_email = settings.EMAIL_HOST_USER
                    to = user.email
                    send_mail(subject, plain_message, from_email, [to], html_message=html_message)
                    return redirect('dashboard')
                except SMTPException:
                    return redirect('dashboard')
    else:
        form = CustomerForm(initial={'user': user, 'referrer': ref})
    context = {'form': form}
    return render(request, 'front/auth/auth-profile.html', context)

def register_view(request):
    context = {}
    user = request.user
    if user.is_authenticated:
        cust = user.customer
        return redirect('dashboard')

    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            act = form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email=email, password=raw_password)
            if account:
                act.save()
                login(request, account)
                return redirect('profile')
            else:
                context['form'] = RegistrationForm(request.POST)
        else:
            context['form'] = RegistrationForm(request.POST)
    else:
        form = RegistrationForm()
        context['form'] = form
    return render(request, 'front/auth/auth-register.html', context)

def register_view_ref(request, ref):
    user = request.user
    context = {}

    try:
        referrer = Customer.objects.get(unique_id=ref)
    except Customer.DoesNotExist:
        ref = 'None'
        referrer = 'None'
        return redirect('register')

    if user.is_authenticated:
        cust = user.customer
        return redirect('dashboard')

    form = RegistrationForm()
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            act = form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email=email, password=raw_password)
            if account:
                act.save()
                login(request, account)
                return redirect('profile')
            else:
                context['form'] = RegistrationForm(request.POST)
        else:
            context['form'] = RegistrationForm(request.POST)
    else:
        form = RegistrationForm(initial={'referrer': ref})
    context = {
        'form': form,
        'referrer': referrer
    }
    return render(request, 'front/auth/auth-register.html', context)

def login_view(request):
    context = {}
    user = request.user
    if user.is_authenticated:
        cust = user.customer
        return redirect('dashboard')

    if request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            account = authenticate(email=email, password=password)

            if account:
                login(request, account)
                pk = request.user.customer.id
                if request.user.is_admin:
                    return redirect('administrator')
                return redirect('dashboard')
        else:
            context['form'] = LoginForm(request.POST)
    else:
        context['form'] = LoginForm()
    return render(request, 'front/auth/auth-login.html', context)

def referral(request):
    if request.POST:
        ref = request.POST['ref']
        return redirect('register_ref', ref)
    return render(request, 'front/auth/auth-ref.html')

def logout_view(request):
    logout(request)
    return redirect('login')