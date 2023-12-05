from django.db import models

# Create your models here.

class PartidasFacade():
    pass

class Observer():
    def update(self):
        pass

class Subject():
    def notifyObservers(self):
        pass

    def registerObserver(self):
        pass

    def removeObserver(self):
        pass

class Partida(Subject):
    def notifyObservers(self):
        pass

    def registerObserver(self):
        pass

    def removeObserver(self):
        pass





    