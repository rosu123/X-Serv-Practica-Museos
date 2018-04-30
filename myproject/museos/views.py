from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import xml.etree.ElementTree as ET
from urllib.request import urlopen


# Create your views here.
XML_URL = 'https://datos.madrid.es/portal/site/egob/menuitem.ac61933d6ee3c31cae77ae7784f1a5a0/?vgnextoid=00149033f2201410VgnVCM100000171f5a0aRCRD&format=xml&file=0&filename=201132-0-museos&mgmtid=118f2fdbecc63410VgnVCM1000000b205a0aRCRD&preview=full'

def xmlParser(req):
    xmlFile = urlopen(XML_URL)
    tree = ET.parse(xmlFile)
    root = tree.getroot()
    #i = 0
    #for child in root.iter('atributo'):
    #    i += 1
    #    print(child.tag, child.attrib)
    #    print("")
    #    if i>6:
    #        break
    for listMuseos in root.iter('contenido'):
        try:
            print("-----------------------------------------")
            for museo in listMuseos.findall('atributos'):
                #name = museos.get('idioma')
                nombre = museo.find('atributo[@nombre="NOMBRE"]').text
                #descripcion = museo.find('atributo[@nombre="DESCRIPCION-ENTIDAD"]').text
                print (nombre)
                #print (name)
        except AttributeError:
            continue

    #for i in root.iter('contenido'):
    #    print (i.tag, i.attrib)

    return HttpResponseRedirect('/')
