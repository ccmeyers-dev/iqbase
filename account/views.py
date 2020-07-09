from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import RegistrationForm, LoginForm, CustomerForm
from broker.views import Customer
from smtplib import SMTPException
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def profile(request):
    user = request.user
    if  user.is_setup:
        return redirect('dashboard')
    cust = user.customer
    form = CustomerForm(initial={'user': cust})
    if request.POST:
        user.is_setup = True
        user.save()
        form = CustomerForm(request.POST, request.FILES, instance=cust)
        if form.is_valid():
            form.save()
            try:
                name = user.first_name
                subject = 'Welcome to IQ Options Trade'
                html_message = render_to_string('front/mail.html', {
                    'name': name,
                    })
                plain_message = strip_tags(html_message)
                from_email = settings.EMAIL_HOST_USER
                to = user.email
                send_mail(subject, plain_message, from_email, [to], html_message=html_message)
                return redirect('dashboard')
            except SMTPException:
                return redirect('dashboard')
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
                return redirect('dashboard')
        else:
            context['form'] = LoginForm(request.POST)
    else:
        context['form'] = LoginForm()
    return render(request, 'front/auth/auth-login.html', context)


def logout_view(request):
    logout(request)
    return redirect('login')

def action_block(request):
    if request.user.is_verified:
        return redirect('dashboard')
    return render(request, 'front/auth/action_block.html')