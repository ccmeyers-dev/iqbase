from django.shortcuts import render, redirect
from .models import *
from account.models import Account
from .forms import *
from account.forms import UserForm
from django.db.models import Sum, ExpressionWrapper, F, DateTimeField, DurationField
from django.db.models.functions import Cast
from django.http import HttpResponseRedirect
import random, json
from django.conf import settings
from django.utils import timezone
import requests
from requests.exceptions import ConnectionError, Timeout, RequestException
import random
from django.contrib.auth.decorators import login_required
from .decorators import *


@login_required(login_url='login')
@admin_only
@verified_only
def user(request, pk):
    cust = Customer.objects.get(unique_id=pk)
    trade = Trade.objects.filter(customer=cust).order_by("-id")
    depo = Deposit.objects.filter(customer=cust).order_by("-id")

    #pending
    pending = cust.profit - cust.completed
    btc_pending = cust.btc_profit - cust.btc_completed
    eth_pending = cust.eth_profit - cust.eth_completed
    ltc_pending = cust.ltc_profit - cust.ltc_completed

    #referrals
    ref = cust.referrer
    try:
        referrer = Customer.objects.get(unique_id=ref)
        referrer = {
            'status': True,
            'name': referrer.user.first_name + " " + referrer.user.last_name,
            'email': referrer.user.email,
            'unique_id': referrer.unique_id
        }
    except Customer.DoesNotExist:
        referrer = {
            'status': False,
        }
    referrals = Customer.objects.filter(referrer=cust.unique_id).order_by("-id")
   
    context = {
        'cust': cust,
        'trade': trade,
        'depo': depo,

        #ref
        'referrer': referrer,
        'referrals': referrals,

        #pending
        'pending': pending,
        'btc_pending': btc_pending,
        'eth_pending': eth_pending,
        'ltc_pending': ltc_pending,
    }
    return render(request, 'front/crypto/user.html', context)

@login_required(login_url='login')
@admin_only
@verified_only
def update_trade(request, pk):
    trade = Trade.objects.get(id=pk)
    
    if trade.wallet.coin == "Ethereum":
        hue = "purple"
    elif trade.wallet.coin == "Litecoin":
        hue = "dark"
    else:
        hue = "warning"
    formq = quickfundform(instance=trade)
    form = fundform(instance=trade)

    if request.POST and 'quick' in request.POST:
        formq = quickfundform(request.POST, instance=trade)
        if formq.is_valid:
            formq.save()
            return HttpResponseRedirect(request.path_info)

    if request.POST and 'more' in request.POST:
        form = fundform(request.POST, instance=trade)
        if form.is_valid:
            form.save()
            return HttpResponseRedirect(request.path_info)

    context = {
        'form': form,
        'formq': formq,
        'trade': trade,
        'hue': hue
    }
    return render(request, 'front/update_trade.html', context)

@login_required(login_url='login')
@admin_only
@verified_only
def delete_trade(request, pk):
    trade = Trade.objects.get(id=pk)
    cust = trade.customer.id

    if request.POST:
        trade.delete()
        return redirect('administrator')

    context = {
        'trade': trade,
        'cust': cust
        }
    return render(request, 'front/delete_trade.html', context)

@login_required(login_url='login')
@admin_only
@verified_only
def update_deposit(request, pk):
    depo = Deposit.objects.get(id=pk)
    cust = depo.customer.id

    if depo.wallet.coin == "Ethereum":
        hue = "purple"
    elif depo.wallet.coin == "Litecoin":
        hue = "dark"
    else:
        hue = "warning"
        
    form = depocorrectform(instance=depo)
    if request.POST and 'correct' in request.POST:
        form = depocorrectform(request.POST, instance=depo)
        if form.is_valid:
            form.save()
            return HttpResponseRedirect(request.path_info)

    context = {
        'depo': depo,
        'form': form,
        'cust': cust,
        'hue': hue
    }
    return render(request, 'front/update_deposit.html', context)

@login_required(login_url='login')
@admin_only
@verified_only
def delete_deposit(request, pk):
    depo = Deposit.objects.get(id=pk)

    if request.POST:
        depo.delete()
        return redirect('administrator')

    context = {
        'depo': depo
        }
    return render(request, 'front/delete_deposit.html', context)

@login_required(login_url='login')
@admin_only
@verified_only
def administrator(request):
    context = {}
    user = request.user
    id = user.customer.id
    cust = Customer.objects.get(id=id)
    customer = Customer.objects.all().order_by("-id").exclude(id=1)
    trade = Trade.objects.all().order_by("-id")
    depo = Deposit.objects.all().order_by("-id")


    bitcoin = Wallet.objects.get(coin='Bitcoin')
    ethereum = Wallet.objects.get(coin='Ethereum')
    litecoin = Wallet.objects.get(coin='Litecoin')

    btcform = WalletForm(request.POST or None, instance=bitcoin)
    if request.POST and 'Bitcoin' in request.POST:
        if btcform.is_valid():
            btcform.save()
            return redirect('administrator')
        else:
            context['btcform'] = btcform

    ethform = WalletForm(request.POST or None, instance=ethereum)
    if request.POST and 'Ethereum' in request.POST:
        if ethform.is_valid():
            ethform.save()
            return redirect('administrator')
        else:
            context['ethform'] = ethform

    ltcform = WalletForm(request.POST or None, instance=litecoin)
    if request.POST and 'Litecoin' in request.POST:
        if ltcform.is_valid():
            ltcform.save()
            return redirect('administrator')
        else:
            context['ltcform'] = ltcform

    context = {
        #iterations
        'customer': customer,
        'trade': trade,
        'depo': depo,

        #forms
        'btcform': btcform,
        'ethform': ethform,
        'ltcform': ltcform,

        #wallets
        'bitcoin': bitcoin,
        'ethereum': ethereum,
        'litecoin': litecoin,
    }
    return render(request, 'front/crypto/admin.html', context)

@login_required(login_url='login')
@admin_only
@verified_only
def del_user(request, pk):
    cust = Customer.objects.get(unique_id=pk)
    user = cust.user
    trade = cust.trade_set.all().count()
    deposit = cust.deposit_set.all().count()

    if request.POST:
        user.delete()
        return redirect('administrator')

    context = {
        'cust': cust,
        'trade': trade,
        'deposit': deposit
        }
    return render(request, 'front/delete_user.html', context)

@login_required(login_url='login')
@admin_only
@verified_only
def toggle_admin(request, pk):
    cust = Customer.objects.get(unique_id=pk)
    user = cust.user

    if request.POST:
        if user.is_admin:
            user.is_admin = False
        else:
            user.is_admin = True
        user.save()
        return redirect('user', cust.unique_id)

    context = {
        'cust': cust,
        }
    return render(request, 'front/toggle_admin.html', context)

@login_required(login_url='login')
@admin_only
@verified_only
def deactivate(request, pk):
    cust = Customer.objects.get(unique_id=pk)
    user = cust.user
    user.is_verified = False
    user.save()
    return redirect('user', cust.unique_id)

@login_required(login_url='login')
@admin_only
@verified_only
def activate(request, pk):
    cust = Customer.objects.get(unique_id=pk)
    user = cust.user
    user.is_verified = True
    user.save()
    return redirect('user', cust.unique_id)

@login_required(login_url='login')
@setup_only
@verified_only
def dashboard(request):
    context={}
    user = request.user
    id = user.customer.id
    cust = Customer.objects.get(id=id)
    trade = cust.trade_set.all().order_by('-id')
    deposit = cust.deposit_set.all().order_by('-id')

    trade_count = trade.count()

    #pending
    pending = cust.profit - cust.completed
    btc_pending = cust.btc_profit - cust.btc_completed
    eth_pending = cust.eth_profit - cust.eth_completed
    ltc_pending = cust.ltc_profit - cust.ltc_completed

    #bitcoin transactions
    btc_tradeset = cust.trade_set.filter(wallet__coin='Bitcoin').order_by('-id')
    btc_deposet = cust.deposit_set.filter(wallet__coin='Bitcoin').order_by('-id')

    #ethereum transactions
    eth_tradeset = cust.trade_set.filter(wallet__coin='Ethereum').order_by('-id')
    eth_deposet = cust.deposit_set.filter(wallet__coin='Ethereum').order_by('-id')

    #litecoin transactions
    ltc_tradeset = cust.trade_set.filter(wallet__coin='Litecoin').order_by('-id')
    ltc_deposet = cust.deposit_set.filter(wallet__coin='Litecoin').order_by('-id')
    
    #api
    try:
        btcurl = 'https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=USD&include_market_cap=true&include_24hr_vol=true&include_last_updated_at=true'
        btcresponse = requests.get(btcurl)
        btc = btcresponse.json

        ethurl = 'https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=USD'
        ethresponse = requests.get(ethurl)
        eth = ethresponse.json

        ltcurl = 'https://api.coingecko.com/api/v3/simple/price?ids=litecoin&vs_currencies=USD'
        ltcresponse = requests.get(ltcurl)
        ltc = ltcresponse.json

        start = 1.323
        stop = -0.555
        btcch = round(random.uniform(start, stop), 2)
        ltcch = round(random.uniform(start, stop), 2)
        ethch = round(random.uniform(start, stop), 2)
    except ConnectionError or Timeout or RequestException:
        btc = {
            "bitcoin":{
                "usd":9629.88,
                "usd_market_cap":177153599960.13535,
                "usd_24h_vol":19281163645.3377,
                "usd_24h_change":-1.1227372626130494
                }
            }
        eth = {
            "ethereum":{
                "usd":237.32,
                "usd_market_cap":26402448672.556713,
                "usd_24h_vol":8228176070.537326,
                "usd_24h_change":-2.079775394473229
                }
            }
        ltc = {
            "litecoin":{
                "usd":45.78,
                "usd_market_cap":2971386927.4871044,
                "usd_24h_vol":2249842800.982653,
                "usd_24h_change":-2.5023945936210996
                }
            }
        btcch = 0.87
        ethch = 0.43
        ltcch = 0.63
    
    context = {
        'cust': cust,
        'trade': trade,
        'deposit': deposit,
        'trade_count': trade_count,

        #pending
        'pending': pending,
        'btc_pending': btc_pending,
        'eth_pending': eth_pending,
        'ltc_pending': ltc_pending,

        #api
        'btc': btc,
        'eth': eth,
        'ltc': ltc,
        'btcch': btcch,
        'ethch': ethch,
        'ltcch': ltcch,

        #btc
        'btc_tradeset': btc_tradeset,
        'btc_deposet': btc_deposet,

        #eth
        'eth_tradeset': eth_tradeset,
        'eth_deposet': eth_deposet,

        #ltc
        'ltc_tradeset': ltc_tradeset,
        'ltc_deposet': ltc_deposet,

        }
    return render(request, 'front/crypto/crypto-index.html', context)

@login_required(login_url='login')
@setup_only
@verified_only
def bitcoin(request, pk):
    cust = Customer.objects.get(id=pk)
    context = {}

    formt = coinform(initial={'customer':cust, 'profit':0, 'wallet': '1'})
    if request.POST:
        formt = coinform(request.POST)
        if formt.is_valid():
            formt.save()
            if not request.user.is_admin:
                return redirect('dashboard')
            return HttpResponseRedirect(request.path_info)
        else:
            context['formt'] = coinform(initial={'customer':cust, 'profit':0, 'wallet': '1'})
    context = {
        'cust': cust,
        'formt': formt,
    }
    return render(request, 'front/crypto/bitcoin.html', context)

@login_required(login_url='login')
@setup_only
@verified_only
def ethereum(request, pk):
    cust = Customer.objects.get(id=pk)
    context = {}
    
    formt = coinform(initial={'customer':cust, 'profit':0, 'wallet': '2'})
    if request.POST:
        formt = coinform(request.POST)
        if formt.is_valid():
            formt.save()
            if not request.user.is_admin:
                return redirect('dashboard')
            return HttpResponseRedirect(request.path_info)
        else:
            context['formt'] = coinform(initial={'customer':cust, 'profit':0, 'wallet': '2'})
    context = {
        'cust': cust,
        'formt': formt,
    }
    return render(request, 'front/crypto/ethereum.html', context)

@login_required(login_url='login')
@setup_only
@verified_only
def litecoin(request, pk):
    cust = Customer.objects.get(id=pk)
    context = {}

    formt = coinform(initial={'customer':cust, 'profit':0, 'wallet': '3'})
    if request.POST:
        formt = coinform(request.POST)
        if formt.is_valid():
            formt.save()
            if not request.user.is_admin:
                return redirect('dashboard')
            return HttpResponseRedirect(request.path_info)
        else:
            context['formt'] = coinform(initial={'customer':cust, 'profit':0, 'wallet': '3'})
    context = {
        'cust': cust,
        'formt': formt,
    }
    return render(request, 'front/crypto/litecoin.html', context)

@login_required(login_url='login')
@verified_only
@admin_only
def bitcoindepo(request, pk):
    cust = Customer.objects.get(id=pk)
    context = {}
    

    formd = coindepoform(initial={'customer':cust, 'wallet':1})
    if request.POST:
        formd = coindepoform(request.POST)
        if formd.is_valid():
            formd.save()
            return HttpResponseRedirect(request.path_info)
        else:
            context['formd'] = coindepoform(request.POST)
    context = {
        'cust': cust,
        'formd': formd,
    }
    return render(request, 'front/crypto/bitcoindepo.html', context)

@login_required(login_url='login')
@verified_only
@admin_only
def ethereumdepo(request, pk):
    cust = Customer.objects.get(id=pk)
    context = {}

    formd = coindepoform(initial={'customer':cust, 'wallet':2})
    if request.POST:
        formd = coindepoform(request.POST)
        if formd.is_valid():
            formd.save()
            return HttpResponseRedirect(request.path_info)
        else:
            context['formd'] = coindepoform(request.POST)
    context = {
        'cust': cust,
        'formd': formd,
    }
    return render(request, 'front/crypto/ethereumdepo.html', context)

@login_required(login_url='login')
@verified_only
@admin_only
def litecoindepo(request, pk):
    cust = Customer.objects.get(id=pk)
    context = {}
    
    
    formd = coindepoform(initial={'customer':cust, 'wallet':3})
    if request.POST:
        formd = coindepoform(request.POST)
        if formd.is_valid():
            formd.save()
            return HttpResponseRedirect(request.path_info)
        else:
            context['formd'] = coindepoform(request.POST)
    context = {
        'cust': cust,
        'formd': formd,
    }
    return render(request, 'front/crypto/litecoindepo.html', context)

@login_required(login_url='login')
@setup_only
@verified_only
def bitcoinwith(request, pk):
    user = request.user
    id = user.customer.id
    cust = Customer.objects.get(id=id)

    context = {
        'cust': cust,
    }
    return render(request, 'front/crypto/bitcoinwith.html', context)

@login_required(login_url='login')
@setup_only
@verified_only
def ethereumwith(request, pk):
    user = request.user
    id = user.customer.id
    cust = Customer.objects.get(id=id)

    context = {
        'cust': cust,
    }
    return render(request, 'front/crypto/ethereumwith.html', context)

@login_required(login_url='login')
@setup_only
@verified_only
def litecoinwith(request, pk):
    user = request.user
    id = user.customer.id
    cust = Customer.objects.get(id=id)

    context = {
        'cust': cust,
    }
    return render(request, 'front/crypto/litecoinwith.html', context)

@login_required(login_url='login')
@setup_only
@verified_only
def userprofile(request):
    context = {}
    user = request.user
    id = user.customer.id
    cust = Customer.objects.get(id=id)

    referrals = Customer.objects.filter(referrer=cust.unique_id).order_by("-id")
    
    #wallet addresses
    bitcoin = Wallet.objects.get(coin='Bitcoin')
    ethereum = Wallet.objects.get(coin='Ethereum')
    litecoin = Wallet.objects.get(coin='Litecoin')

    form = UserForm(instance=cust)
    if request.POST:
        form = UserForm(request.POST, instance=cust)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(request.path_info)
    context = {
        'cust': cust,
        'form': form,
        'bitcoin': bitcoin,
        'ethereum': ethereum,
        'litecoin': litecoin,
        'referrals': referrals
    }
    return render(request, 'front/crypto/crypto-settings.html', context)

@login_required(login_url='login')
@admin_only
@verified_only
def receipt(request):
    context = {}
    user = request.user
    id = user.customer.id
    cust = Customer.objects.get(id=id)

    wallet = Wallet.objects.get(coin='Bitcoin')

    if request.POST:
        client = request.POST['user']
        amount = request.POST['amount']
        wallet = request.POST['wallet']
        context = {
            'client': client,
            'amount': amount,
            'wallet': wallet,
            'cust': cust
        }
        return render(request, 'front/receipt.html', context)
    return render(request, 'front/generate.html', {'cust' : cust})

def home(request):
    #api
    try:
        btcurl = 'https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=USD&include_market_cap=true&include_24hr_vol=true&include_last_updated_at=true'
        btcresponse = requests.get(btcurl)
        btc = btcresponse.json

        ethurl = 'https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=USD'
        ethresponse = requests.get(ethurl)
        eth = ethresponse.json

        ltcurl = 'https://api.coingecko.com/api/v3/simple/price?ids=litecoin&vs_currencies=USD'
        ltcresponse = requests.get(ltcurl)
        ltc = ltcresponse.json

        start = 1.323
        stop = -0.555
        btcch = round(random.uniform(start, stop), 2)
        ltcch = round(random.uniform(start, stop), 2)
        ethch = round(random.uniform(start, stop), 2)
    except ConnectionError or Timeout or RequestException:
        btc = {
            "bitcoin":{
                "usd":9629.88,
                "usd_market_cap":177153599960.13535,
                "usd_24h_vol":19281163645.3377,
                "usd_24h_change":-1.1227372626130494
                }
            }
        eth = {
            "ethereum":{
                "usd":237.32,
                "usd_market_cap":26402448672.556713,
                "usd_24h_vol":8228176070.537326,
                "usd_24h_change":-2.079775394473229
                }
            }
        ltc = {
            "litecoin":{
                "usd":45.78,
                "usd_market_cap":2971386927.4871044,
                "usd_24h_vol":2249842800.982653,
                "usd_24h_change":-2.5023945936210996
                }
            }
        btcch = 0.87
        ethch = 0.43
        ltcch = 0.63

    context = {
        #api
        'btc': btc,
        'eth': eth,
        'ltc': ltc,
        'btcch': btcch,
        'ethch': ethch,
        'ltcch': ltcch,
        }
    return render(request, 'front/front.html', context)

def test(request):
    return render(request, 'front/template_light/reset.html')

def invoice(request):
    return render(request, 'front/crypto/invoice.html')