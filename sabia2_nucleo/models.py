from django.db import models

class Artigo(models.Model):
    titulo = models.CharField(max_length=100, unique=True)
    autor = models.CharField(max_length=100, unique=True)
    resumo = models.TextField()
    tags = models.CharField(max_length=100)
    data = models.DateField(db_index=True, auto_now_add=True)
    categoria = models.ForeignKey('sabia2_nucleo.Categoria')

    def __unicode__(self):
        return '%s' % self.titulo

class Categoria(models.Model):
    titulo = models.CharField(max_length=100, db_index=True)

    def __unicode__(self):
        return '%s' % self.titulo