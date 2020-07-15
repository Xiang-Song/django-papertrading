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
    
        df = yf.download(ticker, start=startday)
        if len(df.index) > 0:
            df1 = df.reset_index()
            plt.clf()
            plt.plot(df1.Date, df1.Close)
            plt.xticks(rotation=30)
            fig = plt.gcf()
            buf = io.BytesIO()
            fig.savefig(buf,format='png')
            buf.seek(0)
            string = base64.b64encode(buf.read())
            uri =  urllib.parse.quote(string)
        else:
            uri = "Error"
        return render(request, 'home.html', {'data': uri})

    else:
        return render(request, 'home.html', {'greeting': "Enter a Ticker Symbol to get infomation"})

   

    
