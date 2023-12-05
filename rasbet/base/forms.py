from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from apostas.models import Utilizador


class conversionForm(forms.Form):
    moeda_origem = forms.CharField(max_length=100)
    moeda_destino = forms.CharField(max_length=100)
    valor = forms.DecimalField(max_digits=16, decimal_places=10)


class createUserForm(UserCreationForm):
    class meta:
        model = User
        fields = ['username', 'password1', 'password2']


class profileForm(forms.ModelForm):
    class Meta:
        model = Utilizador
        fields = ['nome', 'morada', 'codigoPostal', 'nacionalidade', 'email']
        # The labels attribute is optional. It is used to define the labels of the form fields created
        labels = {
            "nome": _("Nome     "),
            "email": _("Email Address"),
            "morada": _("Morada"),
            "codigoPostal": _("Codigo Postal"),
            "nacionalidade": _("Nacionalidade"),
        }
