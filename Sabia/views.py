# coding: utf-8
# Create your views here.
from django.forms import ModelForm
from Sabia.models import *
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.context_processors import csrf
import nltk
import taggit
import summarize

from django.shortcuts import render_to_response
from django.template import RequestContext

def index(request):
    return render_to_response("index.html", RequestContext(request, {}))

def relacionados(request):
    return render_to_response("relacionados.html", RequestContext(request, {}))

class DocumentosModelForm(ModelForm):
    class Meta:
        model = Documento


def autenticar_usuario(request):
    u = {}
    u.update(csrf(request))
    if request.POST:                        
        email = request.POST['email']        
        senha = request.POST['senha']        

        usu = Usuario.objects.filter(email__exact=email)
        usu = usu.filter(senha__exact=senha)

        if usu is not None:
            request.session['usuario_ativo'] = usu


def usuario(request): 
    grupo = Grupo.objects.all()
    return render_to_response("CadastroUsuario.html", {'grupo': grupo}, context_instance=RequestContext(request))
        

def salvar_usuario(request):
    u = {}
    u.update(csrf(request))
    if request.POST:        
        usu = Usuario()        
        usu.nome = request.POST['nome']
        usu.email = request.POST['email']
        usu.senha = request.POST['senha']
        usu.grupo_id = request.POST['grupo_id']
        usu.save()

        grupo = Grupo.objects.all()
        return render_to_response("CadastroUsuario.html", {'grupo': grupo}, context_instance=RequestContext(request))        
        


def documento(request): 
    return render_to_response("CadastroDocumento.html", RequestContext(request, {}))

def salvar_documento(request):
    """Inicia uma nova pergunta"""
    p = request.POST
    if p["titulo"] and p["autor"] and p["resumo_em_html"]:
        #tokenizacao, tagging, removedor de stopwords
        frase = p["titulo"]
        frase = frase.lower()
        tokenizada = nltk.word_tokenize(frase)
        emtags = nltk.tag.pos_tag(tokenizada)
        stopwords = nltk.corpus.stopwords.words('portuguese')
        filtered_words = [w for w in emtags if w not in stopwords]
        #filtra apenas os substantivos
        substantivos = [word for word,pos in filtered_words if 'N' in pos]
        tags = [w for w in substantivos if w not in stopwords]
        #sumariza o resumo
        sumario = summarize.summarize_text(p["resumo_em_html"])
        sumario = sumario.summaries
        sumario = sumario[0]
        doc = Documento.objects.create(titulo=p["titulo"], autor=p["autor"], resumo_em_html=p["resumo_em_html"],
                                       data_publicacao=p["data_publicacao"], classificacao=p["classificacao"], sumario=sumario)
        doc.tag.add(*tags)
    return HttpResponseRedirect(reverse("documento"))