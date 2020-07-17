from django.shortcuts import render, redirect
import matplotlib.pyplot as plt
import io
import urllib, base64
import yfinance as yf
import datetime

from .models import Transactions, Portfolios, Balance
from .forms import TransactionForm, PortfolioForm


def home(request, newContext={}):   #newContext could be used by another view to call this view and update context
    portfolio = Portfolios.objects.all()
    now = datetime.date.today()
    for item in portfolio:
        nowdata = yf.download(item.ticker, start=now)
        nowdata.reset_index(inplace=True)
        nowprice = round(nowdata.iloc[0]['Close'], 2)
        item.price = round(nowprice * item.quantity, 2)
    
    balanc = Balance.objects.get(pk=2)
    cash = balanc.cash

    if request.method == "POST":
        ticker = request.POST['ticker']
        today = datetime.date.today()
        d = datetime.timedelta(days = 30)
        startday = today - d
        todaydata = yf.download(ticker, start=today)
        todaydata.reset_index(inplace=True)
        currentprice = round(todaydata.iloc[0]['Close'], 2) # iloc to retrieve data in particular cell
        monthdata = yf.download(ticker, start=startday)
        if len(monthdata.index) > 0:
            df = monthdata.reset_index()
            plt.clf()   # to clear previous figure
            plt.plot(df.Date, df.Close)
            plt.ylabel('Price (USD)')
            plt.xticks(rotation=15)
            fig = plt.gcf()
            buf = io.BytesIO()
            fig.savefig(buf,format='png')
            buf.seek(0)
            string = base64.b64encode(buf.read())
            uri =  urllib.parse.quote(string)
        else:
            uri = "Error"
        context = {
            'data': uri, 
            'ticker': ticker.upper(), 
            'currentprice': currentprice,
            'cash': cash,
            'portfolio': portfolio
        }
        context.update(newContext)    #update context if this view been called from another view
        return render(request, 'home.html', context)

    else:
        context = {
            'greeting': "Enter a Ticker Symbol to get infomation", 
            'cash': cash,
            'portfolio': portfolio
        }
        context.update(newContext)
        return render(request, 'home.html', context)


def get(request, Portfolios_id):
    item = Portfolios.objects.get(pk=Portfolios_id)
    now = datetime.date.today()
    nowdata = yf.download(item.ticker, start=now)
    nowdata.reset_index(inplace=True)
    item.price = round(nowdata.iloc[0]['Close'], 2)
    context = {
        'selected': item
    }
    response = home(request, context)   #call home view and update context
    return response

def update(request):
    if request.method == "POST":
        form = TransactionForm(request.POST)
        pform = PortfolioForm(request.POST)

        if form.is_valid():
            
            ticker = form.cleaned_data['ticker']   #cleaned_data only available after .is_valid() been called
            quantity = form.cleaned_data['quantity']
            trade = form.cleaned_data['trade']
            price = form.cleaned_data['price']
            balance = Balance.objects.get(pk=2)

            if trade == 'Buy':
                if balance.cash < price * quantity:
                    context = {
                        'warning': "Total price exceed your cash limit!"
                    }
                    response = home(request, context)
                    return response

                balance.cash -= round(price * quantity, 2)
                balance.save()   #always remember to save
            elif trade == 'Sell':
                try:
                    ptfl = Portfolios.objects.get(ticker=ticker)
                    if ptfl.quantity < quantity:
                        context = {
                            'warning': "The quantity exceed your portfolio quantity!"
                        }
                        response = home(request, context)
                        return response
                except:
                    context = {
                        'warning': "You don't have this stock for sell!"
                    }
                    response = home(request, context)
                    return response

                balance.cash += round(price * quantity, 2)
                balance.save()
            form.save()

        if pform.is_valid():
            try:      # it is possible that entry not exist, so use 'try' not 'if', because if entry not exist, django will report error
                entry = Portfolios.objects.get(ticker=ticker)
                if trade == 'Buy':
                    entry.quantity += quantity
                    entry.save()
                elif trade == 'Sell':
                    entry.quantity -= quantity
                    entry.save()
            except:
                pform.save()
    return redirect('home')
   

    
