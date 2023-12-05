from django.urls import path, include

from . import views

urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('register/', views.registerPage, name="register"),
    path('logout/', views.logoutUser, name="logout"),
    path('account/', views.accountPage, name="account"),
    path('conversion/', views.coinConversion, name="conversion"),
    path('apostas/', include('apostas.urls'), name="apostas"),
    path('home/<str:desporto>/', views.home, name="home"),
    path('home/<str:desporto>/<str:sorting>/', views.home, name="homesorting"),
    path('', views.home, name="home"),

]
