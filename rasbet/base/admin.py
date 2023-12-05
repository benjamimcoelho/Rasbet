from django.contrib import admin

from apostas.models import Utilizador, Cambio


# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'nome')


admin.site.register(Utilizador, ProfileAdmin)
admin.site.register(Cambio, admin.ModelAdmin)
