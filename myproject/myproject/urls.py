"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib.auth.views import logout
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'museos.views.barra'),
    url(r'^xml$', 'museos.views.xmlParser'),
    url(r'^borrar', 'museos.views.borrardb'),
    url(r'^comentario/', 'museos.views.cargarComentario'),
    url(r'^acces/', 'museos.views.museosAcc'),
    url(r'^.*style\.css$', 'museos.views.css'),
    url(r'^museos/$', 'museos.views.museosDistrito'),
    url(r'^museos/(\d+)', 'museos.views.detallesMuseo'),
    url(r'^about/$', 'museos.views.about'),
    url(r'^.*login$', 'museos.views.loginView'),
    url(r'^.*logout$', logout, {'next_page': '/'}),
    url(r'^(.*)/xml$', 'museos.views.xmlUser'),
    url(r'^seleccion/(\d+)', 'museos.views.gestionSeleccion'),
    url(r'^deseleccion/(\d+)', 'museos.views.gestionDeseleccion'),
    url(r'^prueba/$', 'museos.views.prueba'),
    url(r'^(.*)$', 'museos.views.user'),
]
