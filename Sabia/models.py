# -*- coding: utf-8 -*-
from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from taggit.managers import TaggableManager

# Create your models here.
class Projeto(models.Model):
    nome  = models.CharField(max_length = 100)
    objetivo = models.TextField()
    palavras_chaves= models.TextField()
    data_cadastro = models.DateField(default=datetime.now, editable=False)

    def __unicode__(self):
        return self.nome

class Grupo(models.Model):
    nome  = models.CharField(max_length = 100)
    projeto_id = models.ForeignKey(Projeto)

    def __unicode__(self):
        return self.nome

class Documento(models.Model):
    titulo = models.CharField(max_length = 100)
    autor = models.CharField(max_length = 100)
    data_publicacao = models.DateField()
    tag = TaggableManager()
    resumo_em_html = models.TextField(blank=True)
    classificacao = models.IntegerField(default=0)
    sumario = models.TextField(blank=True)

    def __unicode__(self):
        return u"%s - %s - %s - %s - %s" % (self.titulo, self.autor, self.tag, self.resumo_em_html, \
               self.classificacao)

class Revisao(models.Model):
    documento = models.ForeignKey(Documento)
    autor = models.ForeignKey(User, blank=False, null=False)
    dtCriacao = models.DateTimeField(auto_now_add=True)
    conteudo = models.TextField()


