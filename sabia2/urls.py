from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Ufes.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', 'Sabia.views.index', name='index'),    
	url(r'^autenticar_usuario/$', 'Sabia.views.autenticar_usuario', name='autenticar_usuario' ),
    
	url(r'^usuario/$', 'Sabia.views.usuario', name='usuario' ), # pagina de cadastro
    url(r'^salvar_usuario/$', 'Sabia.views.salvar_usuario', name='salvar_usuario' ), # pagina de cadastro

    url(r'^documento/$', 'Sabia.views.documento', name='documento' ), # pagina de cadastro
    url(r'^salvar_documento/$', 'Sabia.views.salvar_documento', name='salvar_documento' ), # pagina de cadastro
    url(r'^admin/', include(admin.site.urls)),
)