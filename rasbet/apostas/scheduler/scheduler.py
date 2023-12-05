from statistics import mode
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events
from django.utils import timezone
from django_apscheduler.models import DjangoJobExecution
from apostas.models import ApostaFormula1,ApostaFutebol
import time
import sys
from apostas.scheduler import scheduleCambio, scheduleJogos


def checkForEvents():
    f = open('eventoslog','r')
    lines=f.readlines()
    f.close()
    f = open('eventoslog','w')
    f.close()
    for line in lines:
        list=line.split('/')
        if list[0]=='futebol':
            partida=list[1]
            golos_casa=list[2]
            golos_visitante=list[3]
            ApostaFutebol.partidaEnd(partida,golos_casa,golos_visitante)
        elif list[0]=='formula1':
            partida=list[1]
            vencedor=list[2]
            ApostaFormula1.partidaEnd(partida,vencedor)

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")
    # run this job every 24 hours
    scheduler.add_job(checkForEvents, 'interval', seconds=30, id='EventScheduler' ,replace_existing=True, max_instances=1, name='checkForEvents', jobstore='default')
    scheduler.add_job(scheduleCambio.checkCambio, 'interval', seconds=1800, id='Cambio', replace_existing=True, max_instances=1, name='checkCambio', jobstore='default')
    scheduler.add_job(scheduleJogos.getJogos, 'interval', seconds=86400, id='Jogos', replace_existing=True, max_instances=1, name='checkJogos', jobstore='default')

    scheduleCambio.checkCambio()
    scheduleJogos.getJogos()
    register_events(scheduler)

    #adicionar schedule para adicionar partidas à bd
    #scheduler.add_job(updatePartidas, 'interval', minutes=2, name='checkForEvents', jobstore='default')

    scheduler.start()