from django.contrib import admin
from .models import Transactions, Portfolios, Balance

admin.site.register(Transactions)
admin.site.register(Portfolios)
admin.site.register(Balance)


