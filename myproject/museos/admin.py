from django.contrib import admin

# Register your models here.

from museos.models import Museo
from museos.models import Seleccion
from museos.models import PaginaUser
from museos.models import Comentario
from museos.models import Configuracion

admin.site.register(Museo)
admin.site.register(Seleccion)
admin.site.register(PaginaUser)
admin.site.register(Comentario)
admin.site.register(Configuracion)
