from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Museo(models.Model):
    nombre = models.CharField(max_length=64)
    descripcion = models.TextField(null=True)
    horario = models.TextField(null=True)
    transporte = models.TextField(null=True)
    #accesibilidad = models.BinaryField()
    accesibilidad = models.NullBooleanField(default=False, null=True)
    contentURL = models.URLField(null=True)
    nombreVia = models.CharField(max_length=64, null=True)
    claseVial = models.CharField(max_length=32, null=True)
    numero = models.CharField(max_length=8, null=True)
    localidad = models.CharField(max_length=32, null=True)
    codPostal =  models.CharField(max_length=32, null=True)
    barrio = models.CharField(max_length=64, null=True)
    distrito = models.CharField(max_length=32, null=True)
    telefono = models.TextField(null=True)
    #numero_comentarios = models.IntegerField(default=0)
    email = models.EmailField(null=True)

    def __str__(self):
        return self.nombre + " Accesibilidad: " + str(self.accesibilidad)

    class Meta:
        ordering = ['nombre']


class Seleccion(models.Model):
    museo = models.ForeignKey(Museo)
    user = models.ForeignKey(User)
    fecha = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.user.username + ": " + self.museo.nombre + " " + str(self.fecha)

class PaginaUser(models.Model):
    user = models.ForeignKey(User)
    titulo = models.CharField(max_length=32)

    def __str__(self):
        return self.user.username + ": " + self.titulo



class Comentario(models.Model):
    museo = models.ForeignKey(Museo)
    user = models.ForeignKey(User)
    texto = models.TextField()
    fecha = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.museo.nombre + " " + str(self.fecha)


class Configuracion(models.Model):
    user = models.ForeignKey(User)
    tamano = models.IntegerField()
    letra = models.CharField(max_length=64)
    color = models.CharField(max_length=32)
