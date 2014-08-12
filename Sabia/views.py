# coding: utf-8
# Create your views here.
from django.forms import ModelForm
from Sabia.models import *
from django.http import HttpResponseRedirect
from django.shortcuts import render
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
    return render(request, 'relacionados.html')

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
        
def listar(request):
    documentos = Documento.objects.all()
    context = dict(documentos=documentos, user=request.user)
    return render(request, 'listar.html', context)

def revisao(request, pk):
    """Lista todas as revisoes de um artigo"""
    revisoes = Revisao.objects.filter(documento=pk).order_by("-dtCriacao")
    titulo = Documento.objects.get(pk=pk).titulo
    conteudo = Documento.objects.get(pk=pk).resumo_em_html
    tag = Documento.objects.get(pk=pk).tag
    #carrega as tags em uma lista para serem usadas na pesquisa de relacionados
    tags = []
    for t in tag.all():
        tags.append(str(t))
    #forma a string de pesquisa unindo a lista com uma virgula entre as palavras
    pesquisa = ','.join(tags)
    context = dict(revisoes=revisoes, pk=pk, titulo=titulo, conteudo=conteudo, pesquisa=pesquisa)
    return render(request, 'revisao.html', context)

def detalhe(request, pk):
    """Lista uma revisao de um artigo"""
    revisao = Revisao.objects.get(pk=pk).conteudo
    dtCriacao = Revisao.objects.get(pk=pk).dtCriacao
    autor = Revisao.objects.get(pk=pk).autor
    context = dict(revisao=revisao, autor=autor, dtCriacao=dtCriacao)
    return render(request, 'detalhe.html', context)

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
    return HttpResponseRedirect(reverse("listar"))

def postar(request, ptipo, pk):
    """Exibe um form de post generico"""
    acao = reverse("Sabia.views.%s" % ptipo, args=[pk])
    if ptipo == "revisar":
        titulo = "Revisar"
        destino = Documento.objects.get(pk=pk).titulo
        conteudo = Documento.objects.get(pk=pk).resumo_em_html
    context = dict(destino=destino,acao=acao,titulo=titulo, conteudo=conteudo)
    return render(request, 'postar.html', context)

def revisar(request, pk):
    """Revisa um artigo"""
    p = request.POST
    if p["conteudo"]:
        documento = Documento.objects.get(pk=pk)
        revisao = Revisao.objects.create(documento=documento, conteudo=p["conteudo"],
                                           autor=request.user)
    return HttpResponseRedirect(reverse("revisao", args=[pk]))