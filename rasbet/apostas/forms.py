from django.contrib.auth.forms import UserCreationForm
from django import forms

class dogecoinForm(forms.Form):
        dogecoinwalletaddress = forms.CharField(max_length=100)
        ammount = forms.DecimalField(max_digits=16,decimal_places=10)

class bitcoinForm(forms.Form):
        bitcoinwalletaddress = forms.CharField(max_length=100)
        ammount = forms.DecimalField(max_digits=16,decimal_places=10)

class cardanoForm(forms.Form):
        cardanowalletaddress = forms.CharField(max_length=100)
        ammount = forms.DecimalField(max_digits=16,decimal_places=10)

class euroForm(forms.Form):
        cardnumber = forms.CharField(max_length=100)
        euroammount = forms.DecimalField(max_digits=16,decimal_places=10)

class dolarForm(forms.Form):
        cardnumber = forms.CharField(max_length=100)
        dolarammount = forms.DecimalField(max_digits=16,decimal_places=10)

class libraForm(forms.Form):
        cardnumber = forms.CharField(max_length=100)
        libraammount = forms.DecimalField(max_digits=16,decimal_places=10)

class apostaFutebolBoletimForm(forms.Form):
        moeda = forms.CharField(max_length=100)
        valor = forms.DecimalField(max_digits=16, decimal_places=10)

class apostaFormulaBoletimForm(forms.Form):
        moeda = forms.CharField(max_length=100)
        valor = forms.DecimalField(max_digits=16, decimal_places=10)