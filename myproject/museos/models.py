from django.db import models

# Create your models here.


class Museo(models.Model):
    idEntidad = models.IntegerField()
    nombre = models.CharField(max_length=64)
    descripcion = models.TextField()
    horario = models.TextField()
    transporte = models.TextField()
    #accesibilidad = models.BinaryField()
    accesibilidad = models.BooleanField(default=False)
    contentURL = models.URLField()
    distrito = models.CharField(max_length=32)
    telefono = models.TextField()
    #numero_comentarios = models.IntegerField(default=0)
    email = models.EmailField()

    def __str__(self):
        return self.nombre + " Accesibilidad: " + str(self.accesibilidad)

    class Meta:
        ordering = ['nombre']


class Seleccion(models.Model):
    museo = models.ForeignKey(Museo)
    user = models.CharField(max_length=32)

    #def __str__(self):
    #    return self.user + "(Museo: " + self.museo.nombre + ")"


class Comentario(models.Model):
    museo = models.ForeignKey(Museo)
    texto = models.TextField()
    fecha = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.museo.nombre + " " + str(self.fecha)


class Configuracion(models.Model):
    user = models.CharField(max_length=32)
    titulo_pag = models.CharField(max_length=64)
    tamano = models.IntegerField()
    letra = models.CharField(max_length=64)
    color = models.CharField(max_length=32)
