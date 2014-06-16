from django.db import models

class Artigo(models.Model):
    titulo = models.CharField(max_length=100)
    conteudo = models.TextField()
    resumo = models.CharField(max_length=100)
    tags = models.CharField(max_length=50)