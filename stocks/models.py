from django.db import models
from datetime import date

# Create your models here.
class Transactions(models.Model):
    ticker = models.CharField(max_length = 20)
    trade = models.CharField(max_length = 4, default='Buy')
    quantity = models.IntegerField()
    Date = models.DateField(default=date.today)
    price = models.DecimalField('USD amount', max_digits=8, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return self.ticker

class Portfolios(models.Model):
    ticker = models.CharField(max_length = 20)
    quantity = models.IntegerField()
    price = models.DecimalField('USD amount', max_digits=8, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return self.ticker
    

class Balance(models.Model):
    cash = models.DecimalField('USD amount', default=200000, max_digits=8, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return '{}'.format(self.cash)
         
    