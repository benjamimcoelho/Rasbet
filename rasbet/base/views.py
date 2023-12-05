from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

from apostas.models import ApostaFormula1, Carteira, PartidaFutebol, Utilizador, ApostaFutebol, BoletimCusto, \
    BoletimProfit, PartidaFormula1, Cambio
from .forms import createUserForm, profileForm, conversionForm


def loginPage(request):
    page = 'login'
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password does not exist')

    context = {'page': page}
    return render(request, 'login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')


def registerPage(request):
    page = 'register'
    form = createUserForm()
    profile_form = profileForm()
    if request.method == 'POST':
        form = createUserForm(request.POST)
        profile_form = profileForm(request.POST)

        if form.is_valid() and profile_form.is_valid():
            user = form.save()

            # we don't save the profile_form here because we have to first get the value of profile_form, assign the
            # user to the OneToOneField created in models before we now save the profile_form.

            profile = profile_form.save(commit=False)
            profile.user = user
            wallet = Carteira()
            wallet.save()
            profile.carteira = wallet

            profile.save()

            messages.success(request, 'Your account has been successfully created')

            return redirect('login')

    context = {'form': form, 'profile_form': profile_form, 'page': page}
    return render(request, 'register.html', context)


def accountPage(request):
    context = {}
    if request.user.is_authenticated:
        utilizador = request.user.utilizador
        context["utilizador"] = utilizador
        context["user"] = request.user
        apostasRealizadas = ApostaFutebol.objects.filter(utilizador=utilizador).exclude(estado='B')
        apostasRealizadasFormula = ApostaFormula1.objects.filter(utilizador=utilizador).exclude(estado='B')
        context["apostas"] = apostasRealizadas
        context["apostasFormula"] = apostasRealizadasFormula
        context["metodos"] = Utilizador.getMetodosPagamento()
    return render(request, 'account.html', context)


def coinConversion(request):
    context = {}
    utilizador = request.user.utilizador
    metodos = Utilizador.getMetodosPagamento()
    context["utilizador"] = utilizador
    context["metodos"] = metodos
    if request.method == 'POST':

        form = conversionForm(request.POST)
        # FALSE if user doesnt have enough money
        transaction = True
        if form.is_valid():
            moedaOrigem = form.cleaned_data["moeda_origem"]
            moedaDestino = form.cleaned_data["moeda_destino"]
            valor = form.cleaned_data["valor"]
            # verificar se o utilizador tem guita que chegue
            if moedaOrigem == 'Euro':
                if utilizador.carteira.saldo_euro < valor:
                    transaction = False
                    messages.error(request, 'Não tem fundos suficientes para esta conversão (Euro)')
            elif moedaOrigem == 'Dolar':
                if utilizador.carteira.saldo_dolar < valor:
                    transaction = False
                    messages.error(request, 'Não tem fundos suficientes para esta conversão (Dolar)')
            elif moedaOrigem == 'Dogecoin':
                if utilizador.carteira.saldo_dogecoin < valor:
                    transaction = False
                    messages.error(request, 'Não tem fundos suficientes para esta conversão (Dogecoin)')
            elif moedaOrigem == 'Bitcoin':
                if utilizador.carteira.saldo_bitcoin < valor:
                    transaction = False
                    messages.error(request, 'Não tem fundos suficientes para esta conversão (Bitcoin)')
            elif moedaOrigem == 'Libra':
                if utilizador.carteira.saldo_libra < valor:
                    transaction = False
                    messages.error(request, 'Não tem fundos suficientes para esta conversão (Libra)')
            elif moedaOrigem == 'Cardano':
                if utilizador.carteira.saldo_cardano < valor:
                    transaction = False
                    messages.error(request, 'Não tem fundos suficientes para esta conversão (Cardano)')
            if transaction == True:
                cambio = Cambio.objects.filter(moeda_origem=moedaOrigem).get(moeda_destino=moedaDestino)
                taxa_cambio = cambio.taxa_cambio
                taxa_rasbet = cambio.taxa_rasbet
                novoValor = valor * taxa_cambio
                valorRasbet = novoValor * taxa_rasbet
                novoValor -= valorRasbet
                if moedaOrigem == 'Euro':
                    utilizador.carteira.saldo_euro -= valor
                elif moedaOrigem == 'Dolar':
                    utilizador.carteira.saldo_dolar -= valor
                elif moedaOrigem == 'Dogecoin':
                    utilizador.carteira.saldo_dogecoin -= valor
                elif moedaOrigem == 'Bitcoin':
                    utilizador.carteira.saldo_bitcoin -= valor
                elif moedaOrigem == 'Libra':
                    utilizador.carteira.saldo_libra -= valor
                elif moedaOrigem == 'Cardano':
                    utilizador.carteira.saldo_cardano -= valor
                if moedaDestino == 'Euro':
                    utilizador.carteira.saldo_euro += novoValor
                elif moedaDestino == 'Dolar':
                    utilizador.carteira.saldo_dolar += novoValor
                elif moedaDestino == 'Dogecoin':
                    utilizador.carteira.saldo_dogecoin += novoValor
                elif moedaDestino == 'Bitcoin':
                    utilizador.carteira.saldo_bitcoin += novoValor
                elif moedaDestino == 'Libra':
                    utilizador.carteira.saldo_libra += novoValor
                elif moedaDestino == 'Cardano':
                    utilizador.carteira.saldo_cardano += novoValor
                utilizador.carteira.save()
                messages.success(request, "A conversão foi efetuada com sucesso. Taxa do rasbet: " + str(
                    taxa_rasbet) + ' ( ' + str(valorRasbet) + ' )')

    return render(request, 'conversion.html', context)


# Create your views here.
def home(request, desporto='futebol', sorting='favorite'):
    context = {}
    if desporto == None or desporto == 'futebol':
        if sorting == 'favorite':
            context = {'partidas': PartidaFutebol.objects.filter(estado='A')}
        elif sorting == 'date':
            context = {'partidas': PartidaFutebol.objects.filter(estado='A').order_by('commence_time')}
        elif sorting == 'name':
            context = {'partidas': PartidaFutebol.objects.filter(estado='A').order_by('titulo')}
        context["desporto"] = 'futebol'
    elif desporto == 'formula':
        if sorting == 'favorite':
            context = {'partidasFormula': PartidaFormula1.objects.filter(estado='A')}
        elif sorting == 'date':
            context = {'partidasFormula': PartidaFormula1.objects.filter(estado='A').order_by('commence_time')}
        elif sorting == 'name':
            context = {'partidasFormula': PartidaFormula1.objects.filter(estado='A').order_by('titulo')}
        context["desporto"] = 'formula'
    if request.user.is_authenticated:
        utilizador = request.user.utilizador
        apostasBoletim = ApostaFutebol.objects.filter(utilizador=utilizador.id).filter(estado='B')
        apostasBoletimFormula = ApostaFormula1.objects.filter(utilizador=utilizador.id).filter(estado='B')
        context["utilizador"] = utilizador
        context["apostasBoletim"] = apostasBoletim
        context["apostasBoletimFormula"] = apostasBoletimFormula
        context["metodos"] = Utilizador.getMetodosPagamento()
        context["boletimCustos"] = BoletimCusto.objects.filter(utilizador=utilizador)
        context["boletimProfits"] = BoletimProfit.objects.filter(utilizador=utilizador)

    return render(request, 'home.html', context)
