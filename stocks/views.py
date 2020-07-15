from django.shortcuts import render
import matplotlib.pyplot as plt
import io
import urllib, base64


def home(request):
    import yfinance as yf
    import datetime

    if request.method == "POST":
        ticker = request.POST['ticker']
        today = datetime.date.today()
        d = datetime.timedelta(days = 30)
        startday = today - d
        todaydata = yf.download(ticker, start=today)
        todaydata.reset_index(inplace=True)
        currentprice = round(todaydata.iloc[0]['Close'], 2)
        monthdata = yf.download(ticker, start=startday)
        if len(monthdata.index) > 0:
            df = monthdata.reset_index()
            plt.clf()
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
        return render(request, 'home.html', {'data': uri, 'ticker': ticker.upper(), 'currentprice': currentprice})

    else:
        return render(request, 'home.html', {'greeting': "Enter a Ticker Symbol to get infomation"})

   

    
