# coding: utf-8
# Create your views here.
from django.forms import ModelForm
from Sabia.models import *
from django.http import HttpResponse
from django.core.context_processors import csrf

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.db.models.sql.datastructures import Date

# pagina inicial do projeto django-wars
def index(request):    
    return render_to_response("index.html")



def logout(request):
    try:
        del request.session['usuario_ativo']
    except KeyError:
        pass
    return render_to_response("index.html", {"msg":"Faça novamente o login."})
        
        