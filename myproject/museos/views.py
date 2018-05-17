from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import xml.etree.ElementTree as ET
from urllib.request import urlopen
from museos.models import Museo
from museos.models import Comentario
from museos.models import Seleccion
from museos.models import Configuracion

from museos.forms import nuevoComentario


# Create your views here.
XML_URL = 'https://datos.madrid.es/portal/site/egob/menuitem.ac61933d6ee3c31cae77ae7784f1a5a0/?vgnextoid=00149033f2201410VgnVCM100000171f5a0aRCRD&format=xml&file=0&filename=201132-0-museos&mgmtid=118f2fdbecc63410VgnVCM1000000b205a0aRCRD&preview=full'

def xmlParser(req):
    xmlFile = urlopen(XML_URL)
    tree = ET.parse(xmlFile)
    root = tree.getroot()
    Museo.objects.all().delete()
    for listMuseos in root.iter('contenido'):
        try:
            print("-----------------------------------------")
            for museo in listMuseos.findall('atributos'):
                idEntidad = museo.find('atributo[@nombre="ID-ENTIDAD"]').text
                print (idEntidad)
                nombre = museo.find('atributo[@nombre="NOMBRE"]').text
                print (nombre)
                try:
                    descripcion = museo.find('atributo[@nombre="DESCRIPCION-ENTIDAD"]').text
                except AttributeError:
                    print ("Campo descripcion NO encontrado")
                    pass
                print (descripcion)
                horario = museo.find('atributo[@nombre="HORARIO"]').text
                print (horario)
                transporte = museo.find('atributo[@nombre="TRANSPORTE"]').text
                print (transporte)

                #accesibilidad = int(museo.find('atributo[@nombre="ACCESIBILIDAD"]').text,2)
                if museo.find('atributo[@nombre="ACCESIBILIDAD"]').text == "0":
                    accesibilidad = False
                else:
                    accesibilidad = True
                print (accesibilidad)

                contentURL = museo.find('atributo[@nombre="CONTENT-URL"]').text
                print (contentURL)
                localizacion = museo.find('atributo[@nombre="LOCALIZACION"]')
                try:
                    distrito = localizacion.find('atributo[@nombre="DISTRITO"]').text
                    print (distrito)
                except AttributeError:
                    print ("Campo distrito NO encontrado")
                    pass

                datosContacto = museo.find('atributo[@nombre="DATOSCONTACTOS"]')
                try:
                    telefono = datosContacto.find('atributo[@nombre="TELEFONO"]').text
                    print (telefono)
                except AttributeError:
                    print ("Campo telefono NO encontrado")
                    pass

                numero_comentarios = Comentario.objects.filter(museo__nombre__contains=nombre).count()
                #print ("Numero comentarios: " + str(numero_comentarios))



                try:
                    email = datosContacto.find('atributo[@nombre="EMAIL"]').text
                    print (email)
                except AttributeError:
                    print ("Campo email NO encontrado")
                    pass

        except AttributeError:
            print("***Campo no encontrado para: " + nombre + "***")
            pass



        museo = Museo(idEntidad = idEntidad, nombre = nombre, descripcion = descripcion, horario = horario, transporte = transporte,
                      accesibilidad = accesibilidad, contentURL = contentURL, distrito = distrito, telefono = telefono,
                      numero_comentarios = numero_comentarios, email = email)
        print("!!!!!!!!!!!!!!!!!!!!!!!!! Antes de guardar Museo !!!!!!!!!!!!!!!!!!!!!!!!!")
        museo.save()
        print("!!!!!!!!!!!!!!!!!!!!!!!!! Despues de guardar Museo !!!!!!!!!!!!!!!!!!!!!!!!!")
    #for i in root.iter('contenido'):
    #    print (i.tag, i.attrib)

    resp = "<a href=/xml>Cargar xml</a>"
    return HttpResponse(resp)
    #return HttpResponseRedirect('/')



def cargarComentario(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = nuevoComentario(request.POST)
        # check whether it's valid:
        if form.is_valid():
            nuevo_comentario = Comentario()
            nuevo_comentario.museo = form.cleaned_data['museo']
            nuevo_comentario.texto = form.cleaned_data['comentario']
            #print(form.cleaned_data)
            nuevo_comentario.save()
            ####
            #Actualizar numero de comentraios del museo
            ####

            return HttpResponseRedirect('/thanks/')
        else:
            print("IT IS NOT VALID")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = nuevoComentario()

    context = {'form': form}
    return render(request, 'name.html', context)




'''
@csrf_exempt
def barra(req):
    if request.method == "GET":

        museo = Museo.objects.all()
        aparcs = aparcs.exclude(num_comentarios=0)
        aparcs = aparcs.order_by('-num_comentarios')
        if acc:
            aparcs = aparcs.exclude(accesibilidad=False)
        return aparcs[:5]


        try:
            list_urls = Pages.objects.all()
            resp += "<p>Saved URLs:</p>"
            resp += "<ol>"
            #print(resp)
            for pag in list_urls:
                resp += '<li><a href="' + str(pag.id) + '">' + pag.name + "  (" + pag.page + ')</a></li>'
            resp += "</ol>"
            return HttpResponse(resp)


        return HttpResponse(resp)
'''

'''
def add_comentario(texto, aparcamiento):
    """Añade un comentario a la base de datos"""
    comment = Comentario(texto=texto, aparcamiento=aparcamiento)
    comment.save()
    aparcamiento.num_comentarios += 1
    aparcamiento.save()
'''
