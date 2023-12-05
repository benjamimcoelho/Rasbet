from email import message
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib import messages
from apostas.forms import euroForm, dogecoinForm, dolarForm, bitcoinForm, apostaFutebolBoletimForm, apostaFormulaBoletimForm, cardanoForm,libraForm
from apostas.models import ApostaFormula1, BoletimCusto, Carteira, PartidaFormula1, PartidaFutebol, ApostaFutebol, Piloto, Utilizador, corridaIndividual,EquipasEmpate


# Create your views here.
# request -> response
# request handler
# action
# misleading name (views)

def depositar(request):
    context = {}
    metodos = Utilizador.getMetodosPagamento()
    context['metodos'] = metodos
    if request.method == 'POST':
        form = dogecoinForm(request.POST)
        if form.is_valid():
            wallet = form.cleaned_data['dogecoinwalletaddress']
            ammount = int(form.cleaned_data['ammount'])
            utilizador = request.user.utilizador
            carteira = Carteira.objects.get(utilizador=utilizador)
            carteira.saldo_dogecoin += ammount
            carteira.save()


        else:
            form = euroForm(request.POST)
            if form.is_valid():
                wallet = form.cleaned_data['cardnumber']
                ammount = form.cleaned_data['euroammount']
                utilizador = request.user.utilizador
                carteira = Carteira.objects.get(utilizador=utilizador)
                carteira.saldo_euro += ammount
                carteira.save()

            else:
                form = bitcoinForm(request.POST)
                if form.is_valid():
                    wallet = form.cleaned_data['bitcoinwalletaddress']
                    ammount = int(form.cleaned_data['ammount'])
                    utilizador = request.user.utilizador
                    carteira = Carteira.objects.get(utilizador=utilizador)
                    carteira.saldo_bitcoin += ammount
                    carteira.save()
                else:
                    form = dolarForm(request.POST)
                    if form.is_valid():
                        wallet = form.cleaned_data['cardnumber']
                        ammount = int(form.cleaned_data['dolarammount'])
                        utilizador = request.user.utilizador
                        carteira = Carteira.objects.get(utilizador=utilizador)
                        carteira.saldo_dolar += ammount
                        carteira.save()
                    else:
                        form = libraForm(request.POST)
                        if form.is_valid():
                            wallet = form.cleaned_data['cardnumber']
                            ammount = int(form.cleaned_data['libraammount'])
                            utilizador = request.user.utilizador
                            carteira = Carteira.objects.get(utilizador=utilizador)
                            carteira.saldo_libra += ammount
                            carteira.save()
                        else:
                            form = cardanoForm(request.POST)
                            if form.is_valid():
                                wallet = form.cleaned_data['cardanowalletaddress']
                                ammount = int(form.cleaned_data['ammount'])
                                utilizador = request.user.utilizador
                                carteira = Carteira.objects.get(utilizador=utilizador)
                                carteira.saldo_cardano += ammount
                                carteira.save()
        messages.success(request,"Depósito efetuado com sucesso")
        return redirect('home')
    return render(request, 'depositar.html', context)


def levantar(request):
    context = {}
    metodos = Utilizador.getMetodosPagamento()
    context['metodos'] = metodos
    if request.method == 'POST':
        form = dogecoinForm(request.POST)
        print('OK')
        if form.is_valid():
            wallet = form.cleaned_data['dogecoinwalletaddress']
            ammount = int(form.cleaned_data['ammount'])
            utilizador = request.user.utilizador
            carteira = Carteira.objects.get(utilizador=utilizador)
            carteira.saldo_dogecoin -= ammount
            carteira.save()


        else:
            form = euroForm(request.POST)
            if form.is_valid():
                wallet = form.cleaned_data['cardnumber']
                ammount = form.cleaned_data['euroammount']
                utilizador = request.user.utilizador
                carteira = Carteira.objects.get(utilizador=utilizador)
                carteira.saldo_euro -= ammount
                carteira.save()

            else:
                form = bitcoinForm(request.POST)
                if form.is_valid():
                    wallet = form.cleaned_data['bitcoinwalletaddress']
                    ammount = int(form.cleaned_data['ammount'])
                    utilizador = request.user.utilizador
                    carteira = Carteira.objects.get(utilizador=utilizador)
                    carteira.saldo_bitcoin -= ammount
                    carteira.save()
                else:
                    form = dolarForm(request.POST)
                    if form.is_valid():
                        wallet = form.cleaned_data['cardnumber']
                        ammount = int(form.cleaned_data['dolarammount'])
                        utilizador = request.user.utilizador
                        carteira = Carteira.objects.get(utilizador=utilizador)
                        carteira.saldo_dolar -= ammount
                        carteira.save()
                    else:
                        form = libraForm(request.POST)
                        if form.is_valid():
                            wallet = form.cleaned_data['cardnumber']
                            ammount = int(form.cleaned_data['libraammount'])
                            utilizador = request.user.utilizador
                            carteira = Carteira.objects.get(utilizador=utilizador)
                            carteira.saldo_libra -= ammount
                            carteira.save()
                        else:
                            form = cardanoForm(request.POST)
                            if form.is_valid():
                                wallet = form.cleaned_data['cardanowalletaddress']
                                ammount = int(form.cleaned_data['ammount'])
                                utilizador = request.user.utilizador
                                carteira = Carteira.objects.get(utilizador=utilizador)
                                carteira.saldo_cardano -= ammount
                                carteira.save()
        messages.success(request,"Levantamento efetuado com sucesso")
        return redirect('home')
    return render(request, 'levantar.html', context)

def deleteAposta(request, apostaId):
    ApostaFutebol.objects.filter(id=apostaId).delete()
    utilizador = request.user.utilizador
    utilizador.updateBoletimCustos()
    utilizador.updateBoletimProfits()
    messages.success(request,"Removeu a aposta!")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def deleteApostaFormula(request, apostaId):
    ApostaFormula1.objects.filter(id=apostaId).delete()
    utilizador = request.user.utilizador
    utilizador.updateBoletimCustos()
    utilizador.updateBoletimProfits()
    messages.success(request,"Removeu a aposta!")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def atualizarApostaBoletim(request, apostaId):
    context = {}
    if request.method == 'POST':
        form = apostaFutebolBoletimForm(request.POST)
        if form.is_valid():
            moeda = form.cleaned_data["moeda"]
            valor = form.cleaned_data["valor"]
            aposta = ApostaFutebol.objects.get(id=apostaId)
            aposta.valor = valor
            aposta.moeda = moeda
            aposta.save()
            utilizador = request.user.utilizador
            utilizador.updateBoletimCustos()
            utilizador.updateBoletimProfits()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def atualizarApostaBoletimFormula(request, apostaId):
    context = {}
    if request.method == 'POST':
        form = apostaFormulaBoletimForm(request.POST)
        if form.is_valid():
            moeda = form.cleaned_data["moeda"]
            valor = form.cleaned_data["valor"]
            aposta = ApostaFormula1.objects.get(id=apostaId)
            aposta.valor = valor
            aposta.moeda = moeda
            aposta.save()
            utilizador = request.user.utilizador
            utilizador.updateBoletimCustos()
            utilizador.updateBoletimProfits()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def add_aposta_boletim(request, jogo_id, resultado):
    context = {}
    if request.user.is_authenticated:
        utilizador = request.user.utilizador
        jogo = PartidaFutebol.objects.get(id=jogo_id)
        novaApostaBoletim = ApostaFutebol(valor=0, resultadoApostado=resultado, partida=jogo, estado='B',
                                          utilizador=utilizador)
        novaApostaBoletim.save()
        utilizador.updateBoletimCustos()
        utilizador.updateBoletimProfits()
        messages.success(request,"Aposta adicionada ao boletim!")
    else:
        messages.error(request,"Não tem sessão iniciada")
    return redirect('home','futebol')

def add_aposta_boletim_Formula(request, jogo_id, piloto_id):
    context = {}
    if request.user.is_authenticated:
        utilizador = request.user.utilizador
        jogo = PartidaFormula1.objects.get(id=jogo_id)
        piloto = Piloto.objects.get(id=piloto_id)
        novaApostaBoletim = ApostaFormula1(valor=0, pilotoApostado=piloto, partida=jogo, estado='B',
                                          utilizador=utilizador)
        novaApostaBoletim.save()
        utilizador.updateBoletimCustos()
        utilizador.updateBoletimProfits()
        messages.success(request,"Aposta adicionada ao boletim!")
    return redirect('home','formula')

def limpar_boletim(request):
    context = {}
    if request.user.is_authenticated:
        utilizador = request.user.utilizador
        ApostaFutebol.objects.filter(utilizador=utilizador.id).filter(estado='B').delete()
        ApostaFormula1.objects.filter(utilizador=utilizador.id).filter(estado='B').delete()
        utilizador.updateBoletimCustos()
        utilizador.updateBoletimProfits()
        messages.success(request,"Limpou o boletim!")

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def confirmar_boletim(request):
    context = {}
    if request.user.is_authenticated:
        utilizador = request.user.utilizador
        apostasBoletim = ApostaFutebol.objects.filter(utilizador=utilizador.id).filter(estado='B')
        apostasBoletimFormula = ApostaFormula1.objects.filter(utilizador=utilizador.id).filter(estado='B')
        #flag que representa o estado da transação. caso esta flag fique a falso entao toda a operação é cancelada e é devolvido um erro ao utilizador
        transaction=True
        sent=False

        #verificar o dinheiro do utilizador (caso n tenha fundos retornar mensagem de erro)
        boletimCustos=BoletimCusto.objects.filter(utilizador=utilizador)
        for custo in boletimCustos:
            # se houve erros durante a transação, cancelar
            if transaction==False:
                break
            moeda=custo.moeda
            if custo.valor == 0:
                messages.error(request, 'Alguma aposta não tem valor definido')
                transaction=False
            elif moeda=='Euro':
                if utilizador.carteira.saldo_euro<custo.valor:
                    messages.error(request, 'Não tem fundos suficientes (Euro) para realizar estas apostas')
                    transaction=False
            elif moeda=='Dolar':
                if utilizador.carteira.saldo_dolar<custo.valor:
                    messages.error(request, 'Não tem fundos suficientes (Dolar) para realizar estas apostas')
                    transaction=False
            elif moeda=='Dogecoin':
                if utilizador.carteira.saldo_dogecoin<custo.valor:
                    messages.error(request, 'Não tem fundos suficientes (Dogecoin) para realizar estas apostas')
                    transaction=False
            elif moeda=='Bitcoin':
                if utilizador.carteira.saldo_bitcoin<custo.valor:
                    messages.error(request, 'Não tem fundos suficientes (Bitcoin) para realizar estas apostas')
                    transaction=False
            elif moeda=='Libra':
                if utilizador.carteira.saldo_libra<custo.valor:
                    messages.error(request, 'Não tem fundos suficientes (Libra) para realizar estas apostas')
                    transaction=False
            elif moeda=='Cardano':
                if utilizador.carteira.saldo_cardano<custo.valor:
                    messages.error(request, 'Não tem fundos suficientes (Cardano) para realizar estas apostas')
                    transaction=False

        if transaction==False:
            sent=True

        #retirar dinheiro ao utilizador
        if transaction==True:
            for custo in boletimCustos:
                if moeda=='Euro':
                    utilizador.carteira.saldo_euro-=custo.valor
                elif moeda=='Dolar':
                    utilizador.carteira.saldo_dolar-=custo.valor
                elif moeda=='Dogecoin':
                    utilizador.carteira.saldo_dogecoin-=custo.valor
                elif moeda=='Bitcoin':
                    utilizador.carteira.saldo_bitcoin-=custo.valor
                elif moeda=='Libra':
                    utilizador.carteira.saldo_libra-=custo.valor
                elif moeda=='Cardano':
                    utilizador.carteira.saldo_cardano-=custo.valor
        #se houve um erro durante a transação, cancelar a operação
        if transaction==True:
            for aposta in apostasBoletim:
                #mudar estado dessa aposta
                aposta.estado = 'A'
                #adicionar utilizador aos observadores dessa aposta
                aposta.partida.observadores.add(utilizador)
                aposta.lucro=EquipasEmpate.getProfit(aposta.valor,aposta.resultadoApostado,aposta.partida.odds_casa,aposta.partida.odds_visitante,aposta.partida.odds_empate)
                aposta.save()

        if transaction==True:
            for aposta in apostasBoletimFormula:
                #mudar estado dessa aposta
                aposta.estado = 'A'
                #adicionar utilizador aos observadores dessa aposta
                aposta.partida.observadores.add(utilizador)
                aposta.lucro=corridaIndividual.getProfit(aposta.valor,aposta.pilotoApostado.odds)
                aposta.save()
            messages.success(request,"Boletim confirmado com Sucesso!")
    
        else:
            if sent == False:
                messages.error(request,"Erro ao confirmar o boletim")
        utilizador.updateBoletimCustos()
        utilizador.updateBoletimProfits()
        utilizador.carteira.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def hello(request):
    # pull data from databse
    # transform
    # send email , etc...

    existsPartida = PartidaFutebol.objects.filter(pk=0).exists()

    query_set = PartidaFutebol.objects.all()

    for partida in query_set:
        print(partida)
    return render(request, 'hello.html', {'name': 'Mosh'})
