from django.contrib.auth.models import User
from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields.related import ForeignKey


from partidas.models import Observer, Partida

estado_default = 'A'
estado_finished_win = 'W'
estado_finished_lose = 'L'
estado_suspended = 'S'
estado_boletim = 'B'
estado_choices = [
        (estado_default, 'active'),
        (estado_finished_win, 'win'),
        (estado_finished_lose, 'lose'),
        (estado_suspended, 'suspended'),
        (estado_boletim, 'boletim'),
    ]


jogo_estado_default = 'A'
jogo_estado_finished = 'F'
jogo_estado_choices = [
        (jogo_estado_default, 'active'),
        (jogo_estado_finished, 'finished'),
    ]

moeda_euro = 'E'
moeda_dogecoin = 'D'
moeda_dolar = '$'
moeda_bitcoin = 'B'
moeda_libra = 'L'
moeda_cardano='C'
moedas_choices = [
        (moeda_euro, 'Euro'),
        (moeda_dolar, 'Dolar'),
        (moeda_dogecoin, 'Dogecoin'),
        (moeda_bitcoin, 'Bitcoin'),
        (moeda_cardano, 'Cardano'),
        (moeda_libra, 'Libra'),
    ]

    

# Create your models here.
class UtilizadorFacade():

    def registerCard(self):
        pass

    def registarAposta(self):
        pass

class Cambio(models.Model):
    moeda_origem = models.CharField(max_length=100)
    moeda_destino = models.CharField(max_length=100)
    #taxa de conversao da origem para destino
    taxa_cambio = models.DecimalField(max_digits=16,decimal_places=10)
    #percentagem do valor que fica para o rasbet
    taxa_rasbet = models.DecimalField(max_digits=16,decimal_places=10)

    def update_taxa_cambio(moeda_origem, moeda_destino, taxa_cambio):
        try:
            ori_dest = Cambio.objects.get(moeda_origem=moeda_origem,moeda_destino=moeda_destino)
            dest_ori = Cambio.objects.get(moeda_origem=moeda_destino, moeda_destino=moeda_origem)
            
            new_ori_dest = Cambio(id=ori_dest.id,moeda_origem=moeda_origem, moeda_destino=moeda_destino, taxa_cambio=taxa_cambio,taxa_rasbet=ori_dest.taxa_rasbet)
            new_dest_ori = Cambio(id=dest_ori.id,moeda_origem=moeda_destino, moeda_destino=moeda_origem, taxa_cambio=(1/float(taxa_cambio)), taxa_rasbet=dest_ori.taxa_rasbet)
        except:
            new_ori_dest = Cambio(moeda_origem=moeda_origem, moeda_destino=moeda_destino, taxa_cambio=taxa_cambio,taxa_rasbet=0.03)
            new_dest_ori = Cambio(moeda_origem=moeda_destino, moeda_destino=moeda_origem, taxa_cambio=(1/float(taxa_cambio)), taxa_rasbet=0.03)
        finally:
            new_ori_dest.save()
            new_dest_ori.save()

class Carteira(models.Model):
    saldo_euro = models.DecimalField(max_digits=10, decimal_places=4, default=0)
    saldo_dolar = models.DecimalField(max_digits=10, decimal_places=4, default=0)
    saldo_dogecoin = models.DecimalField(max_digits=16, decimal_places=10, default=0)
    saldo_bitcoin = models.DecimalField(max_digits=16, decimal_places=10, default=0)
    saldo_libra = models.DecimalField(max_digits=16, decimal_places=10, default=0)
    saldo_cardano = models.DecimalField(max_digits=16, decimal_places=10, default=0)



class Utilizador(models.Model, Observer):
    nome = models.CharField(max_length=255)
    morada = models.CharField(max_length=255)
    codigoPostal = models.CharField(max_length=20)
    nacionalidade = models.CharField(max_length=50)
    carteira = models.OneToOneField(Carteira, on_delete=CASCADE)
    email = models.CharField(max_length=255, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # atributo partidas_apostas vem da relacao many to many da classe partidaFutebol

    def update(self):
        pass

    def updateBoletimCustos(self):
        BoletimCusto.objects.filter(utilizador=self).delete()
        apostasFutebol=ApostaFutebol.objects.filter(utilizador=self).filter(estado='B')
        apostasFormula=ApostaFormula1.objects.filter(utilizador=self).filter(estado='B')
        custos={}
        for aposta in apostasFutebol:
            if aposta.moeda not in custos:
                custos[aposta.moeda]=BoletimCusto(moeda=aposta.moeda,valor=aposta.valor,utilizador=self)
            else:
                custos[aposta.moeda].valor+=aposta.valor
        for aposta in apostasFormula:
            if aposta.moeda not in custos:
                custos[aposta.moeda]=BoletimCusto(moeda=aposta.moeda,valor=aposta.valor,utilizador=self)
            else:
                custos[aposta.moeda].valor+=aposta.valor
        for custo in custos:
            custos[custo].save()
            

    def updateBoletimProfits(self):
        BoletimProfit.objects.filter(utilizador=self).delete()
        apostasFutebol=ApostaFutebol.objects.filter(utilizador=self).filter(estado='B')
        apostasFormula=ApostaFormula1.objects.filter(utilizador=self).filter(estado='B')
        profits={}
        for aposta in apostasFutebol:
            if aposta.moeda not in profits:
                profits[aposta.moeda]=BoletimProfit(moeda=aposta.moeda,valor=aposta.getProfit(),utilizador=self)
            else:
                profits[aposta.moeda].valor+=aposta.getProfit()
        for aposta in apostasFormula:
            if aposta.moeda not in profits:
                profits[aposta.moeda]=BoletimProfit(moeda=aposta.moeda,valor=aposta.getProfit(),utilizador=self)
            else:
                profits[aposta.moeda].valor+=aposta.getProfit()
        for profit in profits:
            profits[profit].save()
    
    @staticmethod
    def getMetodosPagamento():
        return(['Euro','Dolar','Dogecoin','Bitcoin','Libra','Cardano'])

class BoletimCusto(models.Model):
    moeda = models.CharField(max_length=100)
    valor = models.DecimalField(max_digits=16,decimal_places=10, default=0)
    utilizador = models.ForeignKey(Utilizador,on_delete=models.CASCADE)

class BoletimProfit(models.Model):
    moeda = models.CharField(max_length=100)
    valor = models.DecimalField(max_digits=16,decimal_places=10, default=0)
    utilizador = models.ForeignKey(Utilizador,on_delete=models.CASCADE)

class CartaoBancario(models.Model):
    numero = models.IntegerField()
    ccv = models.IntegerField()
    expiracao = models.CharField(max_length=10)
    nome = models.CharField(max_length=255)
    utilizador = models.ForeignKey(Utilizador, on_delete=models.CASCADE)


class PartidaFutebol(models.Model, Partida):
    class Meta:
        unique_together = (('equipa_casa','commence_time'),)
    titulo = models.CharField(max_length=255)
    commence_time = models.DateTimeField()
    equipa_casa = models.CharField(max_length=255)
    equipa_visitante = models.CharField(max_length=255)
    odds_casa = models.DecimalField(max_digits=6, decimal_places=2)
    odds_visitante = models.DecimalField(max_digits=6, decimal_places=2)
    observadores = models.ManyToManyField(Utilizador, related_name='partidas_apostadas')
    odds_empate = models.DecimalField(max_digits=6, decimal_places=2, default=1.1)
    estado = models.CharField(max_length=255, choices=jogo_estado_choices, default=jogo_estado_default)

class PartidaFormula1(models.Model,Partida):
    titulo = models.CharField(max_length=255)
    commence_time = models.DateTimeField()
    observadores = models.ManyToManyField(Utilizador, related_name='partidasFormula_apostadas')
    estado = models.CharField(max_length=255, choices=jogo_estado_choices, default=jogo_estado_default)

class Piloto(models.Model):
    nome = models.CharField(max_length=255)
    position = models.IntegerField()
    partida = ForeignKey(PartidaFormula1,on_delete=models.CASCADE)
    odds = models.DecimalField(max_digits=6, decimal_places=2, default=1.1)



class Aposta:
    pass


class ApostaBehaviour:
    def __init__(self):
        pass

    pass

class corridaIndividual(ApostaBehaviour):
    def getProfit(self, valor, odds):
        return valor*odds

    @staticmethod
    def getProfit( valor, odds):
        return valor*odds



class EquipasEmpate(ApostaBehaviour):
    def __init__(self):
        super().__init__()

    def getProfit(self,apostado,resultado, odds_casa, odds_visitante,odds_empate):
        profit=0
        if resultado=='C':
            profit=odds_casa*apostado
        elif resultado=='V':
            profit=odds_visitante*apostado
        elif resultado=='E':
            profit=odds_empate*apostado
        return profit

    @staticmethod
    def getProfit(apostado,resultado, odds_casa, odds_visitante,odds_empate):
        profit=0
        if resultado=='C':
            profit=odds_casa*apostado
        elif resultado=='V':
            profit=odds_visitante*apostado
        elif resultado=='E':
            profit=odds_empate*apostado
        return profit

class ApostaFormula1(models.Model,Aposta):
    moeda = models.CharField(max_length=100, choices=moedas_choices, default=moedas_choices[0][1])
    estado = models.CharField(max_length=20, choices=estado_choices, default=estado_default)
    valor = models.DecimalField(max_digits=16, decimal_places=10)
    partida = ForeignKey(PartidaFormula1, on_delete=models.CASCADE)
    utilizador = ForeignKey(Utilizador, on_delete=models.CASCADE)
    pilotoApostado = ForeignKey(Piloto,on_delete=models.CASCADE)
    lucro = models.DecimalField(max_digits=16,decimal_places=10,default=0)

    behaviour = corridaIndividual()

    def getProfit(self):
        odds = self.pilotoApostado.odds
        return self.behaviour.getProfit(self.valor,odds)
    

    @staticmethod
    def partidaEnd(partida_id,vencedor):
        apostas=ApostaFormula1.objects.filter(partida=partida_id)
        partida=PartidaFormula1.objects.get(id=partida_id)
        partida.estado='F'
        partida.save()
        for aposta in apostas:
            if aposta.pilotoApostado==vencedor:
                aposta.estado="W"
                utilizador=aposta.utilizador
                premio=aposta.getProfit()
                if aposta.moeda=='Euro':
                    utilizador.carteira.saldo_euro+=premio
                elif aposta.moeda=='Dolar':
                    utilizador.carteira.saldo_dolar+=premio
                elif aposta.moeda=='Dogecoin':
                    utilizador.carteira.saldo_dogecoin+=premio
                elif aposta.moeda=='Bitcoin':
                    utilizador.carteira.saldo_bitcoin+=premio
                elif aposta.moeda=='Libra':
                    utilizador.carteira.saldo_libra+=premio
                elif aposta.moeda=='Cardano':
                    utilizador.carteira.saldo_cardano+=premio
                utilizador.carteira.save()
            else:
                aposta.estado='L'
            aposta.save()

class ApostaFutebol(models.Model, Aposta):
    empate = 'E'
    casa = 'C'
    visitante = 'V'
    apostas_choices = [
        (empate, 'empate'),
        (casa, 'casa'),
        (visitante, 'visitante'),
    ]



    moeda = models.CharField(max_length=100, choices=moedas_choices, default=moedas_choices[0][1])
    valor = models.DecimalField(max_digits=16, decimal_places=10)
    resultadoApostado = models.CharField(max_length=100, choices=apostas_choices)
    lucro = models.DecimalField(max_digits=16,decimal_places=10,default=0)

    partida = ForeignKey(PartidaFutebol, on_delete=models.CASCADE)

    estado = models.CharField(max_length=20, choices=estado_choices, default=estado_default)

    utilizador = ForeignKey(Utilizador, on_delete=models.CASCADE)

    behaviour = EquipasEmpate()

    def getProfit(self):
        return self.behaviour.getProfit(self.valor,self.resultadoApostado,self.partida.odds_casa,self.partida.odds_visitante,self.partida.odds_empate)

    def getValor(self):
        pass

    @staticmethod
    def partidaEnd(partida_id,golos_casa,golos_visitante):
        if golos_casa>golos_visitante:
            vencedor='C'
        elif golos_casa==golos_visitante:
            vencedor='E'
        else:
            vencedor='V'
        apostas=ApostaFutebol.objects.filter(partida=partida_id)
        partida=PartidaFutebol.objects.get(id=partida_id)
        partida.estado='F'
        partida.save()
        for aposta in apostas:
            if aposta.resultadoApostado==vencedor:
                aposta.estado="W"
                utilizador=aposta.utilizador
                premio=aposta.getProfit()
                if aposta.moeda=='Euro':
                    utilizador.carteira.saldo_euro+=premio
                elif aposta.moeda=='Dolar':
                    utilizador.carteira.saldo_dolar+=premio
                elif aposta.moeda=='Dogecoin':
                    utilizador.carteira.saldo_dogecoin+=premio
                elif aposta.moeda=='Bitcoin':
                    utilizador.carteira.saldo_bitcoin+=premio
                elif aposta.moeda=='Libra':
                    utilizador.carteira.saldo_libra+=premio
                elif aposta.moeda=='Bitcoin':
                    utilizador.carteira.saldo_cardano+=premio
                utilizador.carteira.save()
            else:
                aposta.estado="L"
            aposta.save()

