from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import xml.etree.ElementTree as ET
from urllib.request import urlopen
from museos.models import Museo


# Create your views here.
XML_URL = 'https://datos.madrid.es/portal/site/egob/menuitem.ac61933d6ee3c31cae77ae7784f1a5a0/?vgnextoid=00149033f2201410VgnVCM100000171f5a0aRCRD&format=xml&file=0&filename=201132-0-museos&mgmtid=118f2fdbecc63410VgnVCM1000000b205a0aRCRD&preview=full'

def xmlParser(req):
    xmlFile = urlopen(XML_URL)
    tree = ET.parse(xmlFile)
    root = tree.getroot()
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
                accesibilidad = int(museo.find('atributo[@nombre="ACCESIBILIDAD"]').text,2)
                print (accesibilidad)
                #if i.find('atributos/atributo[@nombre="ACCESIBILIDAD"]').text == "0":
                #    accesibilidad = False
                #else:
                #    accesibilidad = True
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
                      email = email)
        museo.save()
    #for i in root.iter('contenido'):
    #    print (i.tag, i.attrib)

    resp = "<a href=/xml>Cargar xml</a>"
    return HttpResponse(resp)
    #return HttpResponseRedirect('/')
