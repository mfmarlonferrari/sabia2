# -*- coding: utf-8 -*-
from django.db import models
from datetime import datetime
from taggit.managers import TaggableManager

# Create your models here.
class Projeto(models.Model):
    nome  = models.CharField(max_length = 100)
    objetivo = models.TextField()
    palavras_chaves= models.TextField()
    data_cadastro = models.DateField(default=datetime.now, editable=False)
    
    class Meta:
        db_table = 'Projeto'    
    
    def __unicode__(self):
        return self.nome

class Grupo(models.Model):
    nome  = models.CharField(max_length = 100)    
    projeto_id = models.ForeignKey(Projeto)
    
    class Meta:
        db_table = 'Grupo'
        
    def __unicode__(self):
        return self.nome

class Usuario(models.Model):
    nome  = models.CharField(max_length = 100)
    email = models.CharField(max_length = 100)
    senha = models.CharField(max_length = 20)
    grupo = models.ForeignKey(Grupo)
    
    
    class Meta:
        db_table = 'Usuario'
        
    def __unicode__(self):
        return self.nome

class Documento(models.Model):
    titulo = models.CharField(max_length = 100)
    autor = models.CharField(max_length = 100)
    data_publicacao = models.CharField(max_length = 10)
    tag = TaggableManager()
    arquivo = models.BinaryField()
    resumo_em_html = models.TextField(blank=True)
    classificacao = models.IntegerField(default=0)
    sumario = models.TextField(blank=True)
    
    class Meta:
        db_table = 'Documento'

    def __unicode__(self):
        return u"%s - %s - %s - %s - %s - %s" % (self.titulo, self.autor, self.tag, self.arquivo, self.resumo_em_html, \
               self.classificacao)