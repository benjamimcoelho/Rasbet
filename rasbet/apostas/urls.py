from django.urls import include,path
from . import views
from base.views import registerPage



# URLConf
urlpatterns = [
    path('hello/', views.hello),
    path('addapostaboletim/<int:jogo_id>/<str:resultado>/',views.add_aposta_boletim,name="add-aposta-boletim"),
    path('addapostaboletimFormula/<int:jogo_id>/<int:piloto_id>/',views.add_aposta_boletim_Formula,name="add-aposta-boletim-formula"),
    path('atualizarApostaBoletim/<int:apostaId>/',views.atualizarApostaBoletim,name="atualizarApostaBoletim"),
    path('atualizarApostaBoletimFormula/<int:apostaId>/',views.atualizarApostaBoletimFormula,name="atualizarApostaBoletimFormula"),
    path('deleteAposta/<int:apostaId>/',views.deleteAposta,name="deleteAposta"),
    path('deleteApostaFormula/<int:apostaId>/',views.deleteApostaFormula,name="deleteApostaFormula"),
    path('limparboletim/',views.limpar_boletim,name="limparboletim"),
    path('confirmarboletim/',views.confirmar_boletim,name="confirmarboletim"),
    path('depositar/',views.depositar,name="depositar"),
    path('levantar/',views.levantar,name="levantar"),
    path('registar/',registerPage,name="registar"),
]