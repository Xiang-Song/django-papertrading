from django import forms
from .models import Transactions, Portfolios


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transactions
        fields = ('ticker', 'trade', 'quantity', 'price')


class PortfolioForm(forms.ModelForm):
    class Meta:
        model = Portfolios
        fields = ('ticker', 'quantity')