from django.shortcuts import render, redirect
from .models import *
from account.models import Account
from .forms import *
from account.forms import UserForm
from django.db.models import Sum
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
    cust = Customer.objects.get(id=pk)
    trade = Trade.objects.filter(customer=cust).order_by("-id")
    depo = Deposit.objects.filter(customer=cust).order_by("-id")

    context = {
        'cust': cust,
        'trade': trade,
        'depo': depo,
    }
    return render(request, 'front/crypto/user.html', context)

@login_required(login_url='login')
@admin_only
@verified_only
def update_trade(request, pk):
    trade = Trade.objects.get(id=pk)

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
        'trade': trade
    }
    return render(request, 'front/update_trade.html', context)

@login_required(login_url='login')
@admin_only
@verified_only
def delete_trade(request, pk):
    trade = Trade.objects.get(id=pk)
    cust = trade.customer.id

    # Trade.delete()
    # return redirect('home')

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

    if request.POST and 'confirm' in request.POST:
        depo.status = 'Confirmed'
        depo.save()

    if request.POST and 'cancel' in request.POST:
        depo.status = 'Cancelled'
        depo.save()

    if request.POST and 'pend' in request.POST:
        depo.status = 'Pending'
        depo.save()

    form = depocorrectform(instance=depo)
    if request.POST and 'correct' in request.POST:
        form = depocorrectform(request.POST, instance=depo)
        if form.is_valid:
            form.save()
            return HttpResponseRedirect(request.path_info)

    context = {
        'depo': depo,
        'form': form,
        'cust': cust
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
        'cust': cust,
        'customer': customer,
        'trade': trade,
        'depo': depo,
        'btcform': btcform,
        'ethform': ethform,
        'ltcform': ltcform,
        'bitcoin': bitcoin,
        'ethereum': ethereum,
        'litecoin': litecoin,
    }
    return render(request, 'front/crypto/admin.html', context)

@login_required(login_url='login')
@admin_only
@verified_only
def del_user(request, pk):
    user = Account.objects.get(id=pk)
    user.delete()
    return redirect('administrator')

@login_required(login_url='login')
@admin_only
@verified_only
def deactivate(request, pk):
    user = Account.objects.get(id=pk)
    user.is_verified = False
    user.save()
    return redirect('user', user.customer.id)

@login_required(login_url='login')
@admin_only
@verified_only
def activate(request, pk):
    user = Account.objects.get(id=pk)
    user.is_verified = True
    user.save()
    return redirect('user', user.customer.id)

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
    t = cust.trade
    p = cust.profit
    d = cust.deposit
    balance = cust.balance

    #bitcoin transactions
    btc_tradeset = cust.trade_set.filter(wallet__coin='Bitcoin').order_by('-id')
    btc_deposet = cust.deposit_set.filter(wallet__coin='Bitcoin', status='Confirmed').order_by('-id')
    #pendingdeposit
    btc_pending = cust.deposit_set.filter(wallet__coin='Bitcoin', status='Pending').order_by('-id').aggregate(Sum('amount'))['amount__sum'] or 0

    btc_amount = btc_tradeset.aggregate(Sum('amount'))['amount__sum'] or 0
    btc_profit = btc_tradeset.aggregate(Sum('profit'))['profit__sum'] or 0
    btc_deposit = btc_deposet.aggregate(Sum('amount'))['amount__sum'] or 0
    btc_balance = btc_deposit - btc_amount + btc_profit

    #ethereum transactions
    eth_tradeset = cust.trade_set.filter(wallet__coin='Ethereum').order_by('-id')
    eth_deposet = cust.deposit_set.filter(wallet__coin='Ethereum', status='Confirmed').order_by('-id')
    #pendingdeposit
    eth_pending = cust.deposit_set.filter(wallet__coin='Ethereum', status='Pending').order_by('-id').aggregate(Sum('amount'))['amount__sum'] or 0

    eth_amount = eth_tradeset.aggregate(Sum('amount'))['amount__sum'] or 0
    eth_profit = eth_tradeset.aggregate(Sum('profit'))['profit__sum'] or 0
    eth_deposit = eth_deposet.aggregate(Sum('amount'))['amount__sum'] or 0
    eth_balance = eth_deposit - eth_amount + eth_profit

    #litecoin transactions
    ltc_tradeset = cust.trade_set.filter(wallet__coin='Litecoin').order_by('-id')
    ltc_deposet = cust.deposit_set.filter(wallet__coin='Litecoin', status='Confirmed').order_by('-id')
    #pendingdeposit
    ltc_pending = cust.deposit_set.filter(wallet__coin='Litecoin', status='Pending').order_by('-id').aggregate(Sum('amount'))['amount__sum'] or 0

    ltc_amount = ltc_tradeset.aggregate(Sum('amount'))['amount__sum'] or 0
    ltc_profit = ltc_tradeset.aggregate(Sum('profit'))['profit__sum'] or 0
    ltc_deposit = ltc_deposet.aggregate(Sum('amount'))['amount__sum'] or 0
    ltc_balance = ltc_deposit - ltc_amount + ltc_profit

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
        't': t,
        'p': p,
        'd': d,
        'balance': balance,
        'trade': trade,
        'deposit': deposit,

        #api
        'btc': btc,
        'eth': eth,
        'ltc': ltc,
        'btcch': btcch,
        'ethch': ethch,
        'ltcch': ltcch,

        #pending
        'btc_pending': btc_pending,
        'eth_pending': eth_pending,
        'ltc_pending': ltc_pending,

        #btc
        'btc_tradeset': btc_tradeset,
        'btc_deposet': btc_deposet,
        'btc_amount': btc_amount,
        'btc_profit': btc_profit,
        'btc_deposit': btc_deposit,
        'btc_balance': btc_balance,

        #eth
        'eth_tradeset': eth_tradeset,
        'eth_deposet': eth_deposet,
        'eth_amount': eth_amount,
        'eth_profit': eth_profit,
        'eth_deposit': eth_deposit,
        'eth_balance': eth_balance,

        #ltc
        'ltc_tradeset': ltc_tradeset,
        'ltc_deposet': ltc_deposet,
        'ltc_amount': ltc_amount,
        'ltc_profit': ltc_profit,
        'ltc_deposit': ltc_deposit,
        'ltc_balance': ltc_balance,

        }
    return render(request, 'front/crypto/crypto-index.html', context)

@login_required(login_url='login')
@verified_only
def bitcoin(request, pk):
    user = request.user
    id = user.customer.id
    cust = Customer.objects.get(id=id)

    #bitcoin transactions
    btc_tradeset = cust.trade_set.filter(wallet__coin='Bitcoin').order_by('-id')
    btc_deposet = cust.deposit_set.filter(wallet__coin='Bitcoin', status='Confirmed').order_by('-id')
    btc_amount = btc_tradeset.aggregate(Sum('amount'))['amount__sum'] or 0
    btc_profit = btc_tradeset.aggregate(Sum('profit'))['profit__sum'] or 0
    btc_deposit = btc_deposet.aggregate(Sum('amount'))['amount__sum'] or 0
    btc_balance = btc_deposit - btc_amount + btc_profit

    formt = coinform(initial={'customer':cust,'status':'Pending', 'profit':0, 'wallet': '1'})
    if request.POST:
        formt = coinform(request.POST)
        if formt.is_valid():
            formt.save()
            return redirect('dashboard')
        else:
            context['formt'] = formt
    context = {
        'cust': cust,
        'formt': formt,
        #btc
        'btc_tradeset': btc_tradeset,
        'btc_deposet': btc_deposet,
        'btc_amount': btc_amount,
        'btc_profit': btc_profit,
        'btc_deposit': btc_deposit,
        'btc_balance': btc_balance,
    }
    return render(request, 'front/crypto/bitcoin.html', context)

@login_required(login_url='login')
@verified_only
def ethereum(request, pk):
    user = request.user
    id = user.customer.id
    cust = Customer.objects.get(id=id)

    #ethereum transactions
    eth_tradeset = cust.trade_set.filter(wallet__coin='Ethereum').order_by('-id')
    eth_deposet = cust.deposit_set.filter(wallet__coin='Ethereum', status='Confirmed').order_by('-id')
    eth_amount = eth_tradeset.aggregate(Sum('amount'))['amount__sum'] or 0
    eth_profit = eth_tradeset.aggregate(Sum('profit'))['profit__sum'] or 0
    eth_deposit = eth_deposet.aggregate(Sum('amount'))['amount__sum'] or 0
    eth_balance = eth_deposit - eth_amount + eth_profit

    formt = coinform(initial={'customer':cust,'status':'Pending', 'profit':0, 'wallet': '2'})
    if request.POST:
        formt = coinform(request.POST)
        if formt.is_valid():
            formt.save()
            return redirect('dashboard')
        else:
            context['formt'] = formt
    context = {
        'cust': cust,
        'formt': formt,
        #eth
        'eth_tradeset': eth_tradeset,
        'eth_deposet': eth_deposet,
        'eth_amount': eth_amount,
        'eth_profit': eth_profit,
        'eth_deposit': eth_deposit,
        'eth_balance': eth_balance,
    }
    return render(request, 'front/crypto/ethereum.html', context)

@login_required(login_url='login')
@verified_only
def litecoin(request, pk):
    user = request.user
    id = user.customer.id
    cust = Customer.objects.get(id=id)

    #litecoin transactions
    ltc_tradeset = cust.trade_set.filter(wallet__coin='Litecoin').order_by('-id')
    ltc_deposet = cust.deposit_set.filter(wallet__coin='Litecoin', status='Confirmed').order_by('-id')
    ltc_amount = ltc_tradeset.aggregate(Sum('amount'))['amount__sum'] or 0
    ltc_profit = ltc_tradeset.aggregate(Sum('profit'))['profit__sum'] or 0
    ltc_deposit = ltc_deposet.aggregate(Sum('amount'))['amount__sum'] or 0
    ltc_balance = ltc_deposit - ltc_amount + ltc_profit

    formt = coinform(initial={'customer':cust,'status':'Pending', 'profit':0, 'wallet': '3'})
    if request.POST:
        formt = coinform(request.POST)
        if formt.is_valid():
            formt.save()
            return redirect('dashboard')
        else:
            context['formt'] = formt
    context = {
        'cust': cust,
        'formt': formt,
        #ltc
        'ltc_tradeset': ltc_tradeset,
        'ltc_deposet': ltc_deposet,
        'ltc_amount': ltc_amount,
        'ltc_profit': ltc_profit,
        'ltc_deposit': ltc_deposit,
        'ltc_balance': ltc_balance,
    }
    return render(request, 'front/crypto/litecoin.html', context)

@login_required(login_url='login')
@verified_only
def bitcoindepo(request, pk):
    user = request.user
    id = user.customer.id
    cust = Customer.objects.get(id=id)

    wallet = Wallet.objects.get(coin='Bitcoin')

    formd = coindepoform(initial={'customer':cust, 'status':'Pending', 'wallet':1})
    if request.POST:
        formd = coindepoform(request.POST)
        if formd.is_valid():
            formd.save()
            trade = request.POST['amount']
            rand = random.randint(103030, 903030)
            context = {
                'rand': rand,
                'trade': trade,
                'cust': cust,
                'wallet': wallet,
            }
            return render(request, 'front/crypto/invoice.html', context)
        else:
            context['formd'] = formd
    context = {
        'cust': cust,
        'formd': formd,
        'wallet': wallet,
    }
    return render(request, 'front/crypto/bitcoindepo.html', context)

@login_required(login_url='login')
@verified_only
def ethereumdepo(request, pk):
    user = request.user
    id = user.customer.id
    cust = Customer.objects.get(id=id)

    wallet = Wallet.objects.get(coin='Ethereum')

    formd = coindepoform(initial={'customer':cust, 'status':'Pending', 'wallet':2})
    if request.POST:
        formd = coindepoform(request.POST)
        if formd.is_valid():
            formd.save()
            trade = request.POST['amount']
            rand = random.randint(103030, 903030)
            context = {
                'rand': rand,
                'trade': trade,
                'cust': cust,
                'wallet': wallet,
            }
            return render(request, 'front/crypto/invoice.html', context)
        else:
            context['formd'] = formd
    context = {
        'cust': cust,
        'formd': formd,
        'wallet': wallet,
    }
    return render(request, 'front/crypto/ethereumdepo.html', context)

@login_required(login_url='login')
@verified_only
def litecoindepo(request, pk):
    user = request.user
    id = user.customer.id
    cust = Customer.objects.get(id=id)

    wallet = Wallet.objects.get(coin='Litecoin')

    formd = coindepoform(initial={'customer':cust, 'status':'Pending', 'wallet':3})
    if request.POST:
        formd = coindepoform(request.POST)
        if formd.is_valid():
            formd.save()
            trade = request.POST['amount']
            rand = random.randint(103030, 903030)
            context = {
                'rand': rand,
                'trade': trade,
                'cust': cust,
                'wallet': wallet,
            }
            return render(request, 'front/crypto/invoice.html', context)
        else:
            context['formd'] = formd
    context = {
        'cust': cust,
        'formd': formd,
        'wallet': wallet,
    }
    return render(request, 'front/crypto/litecoindepo.html', context)

@login_required(login_url='login')
@verified_only
def bitcoinwith(request, pk):
    user = request.user
    id = user.customer.id
    cust = Customer.objects.get(id=id)

    #bitcoin transactions
    btc_tradeset = cust.trade_set.filter(wallet__coin='Bitcoin').order_by('-id')
    btc_deposet = cust.deposit_set.filter(wallet__coin='Bitcoin', status='Confirmed').order_by('-id')
    btc_amount = btc_tradeset.aggregate(Sum('amount'))['amount__sum'] or 0
    btc_profit = btc_tradeset.aggregate(Sum('profit'))['profit__sum'] or 0
    btc_deposit = btc_deposet.aggregate(Sum('amount'))['amount__sum'] or 0
    btc_balance = btc_deposit - btc_amount + btc_profit

    context = {
        'cust': cust,
        #btc
        'btc_tradeset': btc_tradeset,
        'btc_deposet': btc_deposet,
        'btc_amount': btc_amount,
        'btc_profit': btc_profit,
        'btc_deposit': btc_deposit,
        'btc_balance': btc_balance,
    }
    return render(request, 'front/crypto/bitcoinwith.html', context)

@login_required(login_url='login')
@verified_only
def ethereumwith(request, pk):
    user = request.user
    id = user.customer.id
    cust = Customer.objects.get(id=id)

    #ethereum transactions
    eth_tradeset = cust.trade_set.filter(wallet__coin='Ethereum').order_by('-id')
    eth_deposet = cust.deposit_set.filter(wallet__coin='Ethereum', status='Confirmed').order_by('-id')
    eth_amount = eth_tradeset.aggregate(Sum('amount'))['amount__sum'] or 0
    eth_profit = eth_tradeset.aggregate(Sum('profit'))['profit__sum'] or 0
    eth_deposit = eth_deposet.aggregate(Sum('amount'))['amount__sum'] or 0
    eth_balance = eth_deposit - eth_amount + eth_profit

    context = {
        'cust': cust,
        #eth
        'eth_tradeset': eth_tradeset,
        'eth_deposet': eth_deposet,
        'eth_amount': eth_amount,
        'eth_profit': eth_profit,
        'eth_deposit': eth_deposit,
        'eth_balance': eth_balance,
    }
    return render(request, 'front/crypto/ethereumwith.html', context)

@login_required(login_url='login')
@verified_only
def litecoinwith(request, pk):
    user = request.user
    id = user.customer.id
    cust = Customer.objects.get(id=id)

    #litecoin transactions
    ltc_tradeset = cust.trade_set.filter(wallet__coin='Litecoin').order_by('-id')
    ltc_deposet = cust.deposit_set.filter(wallet__coin='Litecoin', status='Confirmed').order_by('-id')
    ltc_amount = ltc_tradeset.aggregate(Sum('amount'))['amount__sum'] or 0
    ltc_profit = ltc_tradeset.aggregate(Sum('profit'))['profit__sum'] or 0
    ltc_deposit = ltc_deposet.aggregate(Sum('amount'))['amount__sum'] or 0
    ltc_balance = ltc_deposit - ltc_amount + ltc_profit

    context = {
        'cust': cust,
        #ltc
        'ltc_tradeset': ltc_tradeset,
        'ltc_deposet': ltc_deposet,
        'ltc_amount': ltc_amount,
        'ltc_profit': ltc_profit,
        'ltc_deposit': ltc_deposit,
        'ltc_balance': ltc_balance,
    }
    return render(request, 'front/crypto/litecoinwith.html', context)

@login_required(login_url='login')
@verified_only
def userprofile(request):
    context = {}
    user = request.user
    id = user.customer.id
    cust = Customer.objects.get(id=id)

    form = UserForm(instance=cust)
    if request.POST:
        form = UserForm(request.POST, instance=cust)
        if form.is_valid():
            form.save()
    context = {
        'cust': cust,
        'form': form
    }
    return render(request, 'front/crypto/crypto-settings.html', context)

@login_required(login_url='login')
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
