from django.contrib import admin

# Register your models here.
from Sabia.models import Projeto, Grupo, Documento

admin.site.register(Projeto)
admin.site.register(Grupo)
admin.site.register(Documento)
