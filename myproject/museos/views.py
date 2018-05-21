from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import xml.etree.ElementTree as ET
from urllib.request import urlopen
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from sqlite3 import OperationalError
from django.db.models import Count

from museos.models import Museo
from museos.models import Comentario
from museos.models import Seleccion
from museos.models import PaginaUser
from museos.models import Configuracion

from museos.forms import nuevoComentario
from museos.forms import filtrarDistrito


# Create your views here.
XML_URL = 'https://datos.madrid.es/portal/site/egob/menuitem.ac61933d6ee3c31cae77ae7784f1a5a0/?vgnextoid=00149033f2201410VgnVCM100000171f5a0aRCRD&format=xml&file=0&filename=201132-0-museos&mgmtid=118f2fdbecc63410VgnVCM1000000b205a0aRCRD&preview=full'
TAMANO_CSS_DEFAULT = '14px'
COLOR_CSS_DEFAULT = '#FFFFFF'


def insertar_atributo_xml(child, atributo, valor):
    atrib = ET.SubElement(child, 'atributo', {'nombre': atributo})
    atrib.text = valor

def insertar_museo_xml(child, museo):
    insertar_atributo_xml(child, "NOMBRE", str(museo.nombre))
    insertar_atributo_xml(child, "DESCRIPCION", str(museo.descripcion))
    insertar_atributo_xml(child, "HORARIO", str(museo.horario))
    insertar_atributo_xml(child, "TRANSPORTE", str(museo.transporte))
    insertar_atributo_xml(child, "ACCESIBILIDAD", str(museo.accesibilidad))
    insertar_atributo_xml(child, "URL", str(museo.contentURL))
    insertar_atributo_xml(child, "DIRECCION", str(museo.claseVial) + " " + str(museo.nombreVia) + " " + str(museo.numero) + ", " + str(museo.codPostal) + " " + str(museo.localidad))
    insertar_atributo_xml(child, "BARRIO", str(museo.barrio))
    insertar_atributo_xml(child, "DISTRITO", str(museo.distrito))
    insertar_atributo_xml(child, "CONTACTO", str(museo.telefono) + " / " + str(museo.email))

#Ayuda: https://pymotw.com/2/xml/etree/ElementTree/create.html
def xmlUser(request, username):
    root = ET.Element('Contenidos')
    selec = Seleccion.objects.filter(user__username=username)
    for i in selec:
        child = ET.SubElement(root, 'museo')
        insertar_museo_xml(child, i.museo)
    return HttpResponse(ET.tostring(root), content_type="text/xml")


def css(request):
    #template = get_template("style.css")
    username = request.user.get_username()
    print("LLAMO A CSS")
    try:
        conf_user = Configuracion.objects.get(user__username=username)
        color = conf_user.color
        tamano = conf_user.tamano
    except ObjectDoesNotExist:
        color = COLOR_CSS_DEFAULT
        tamano = TAMANO_CSS_DEFAULT
    context = {'tam': str(tamano), 'color': color}
    return HttpResponse(render(request, 'style.css', context), content_type="text/css")


def actualizarDatos(request,username):
    titulo = request.POST.get('titulo', False)
    print("Titulo: " + str(titulo))
    if titulo:
        PaginaUser.objects.filter(user__username=username).update(titulo=titulo)
    else:
        print("Titulo vacio")


def actualizarEstilo(request,username):
    color_css = request.POST.get('color_css')
    tamano_css = request.POST.get('tamano_css')
    if color_css and tamano_css:
        print("Nuevos tamaño y color en CSS")
        try:
            conf_user = Configuracion.objects.get(user__username=username)
            Configuracion.objects.filter(user__username=username).update(tamano=tamano_css, color=color_css)

        except ObjectDoesNotExist:
            conf_usuario = Configuracion(user=username, tamano=tamano_css, color=color_css)
            conf_usuario.save()
    else:
        print("No se actualiza CSS")


@csrf_exempt
def user(request, username):
    #user = User.objects.get(username=request.user.username)
    #global acc
    selec = Seleccion.objects.filter(user__username=username)
    try:
        user = User.objects.get(username=username)
        found = True
    except ObjectDoesNotExist:
        found = False

    #if acc:
    #    selec = selec.exclude(museo__accesibilidad=False)
    ultima = False
    try:
        pag = int(request.GET['pag'])
        if pag <= 0:
            pag = 1
    except KeyError:
        pag = 1
    inicio = (pag - 1) * 5
    fin = pag * 5
    if fin >= len(selec):
        fin = len(selec)
        ultima = True

    if request.method == "POST" and request.user.is_authenticated():
        actualizarDatos(request,username)
        actualizarEstilo(request,user)

    titulo = PaginaUser.objects.get(user__username=username)

    userpropio = request.user.is_authenticated() and (username == request.user.username)

    print("¿SOY EL DUEÑO?: " + str(userpropio))
    context = {'aut': request.user.is_authenticated(), 'name': request.user.username, 'found': found,
                'selecciones': selec[inicio:fin], 'ultima': ultima, 'primera': (pag == 1),
                'pag_sig': str(pag + 1), 'pag_ant': str(pag - 1), 'username': username,
                'userpropio': userpropio,'titulo': titulo}
    return render(request, 'users.html', context)







def museosAcc(request):
    museos_accesibles = Museo.objects.filter(accesibilidad=True)
    #resp = "<ol>"
    #for museo in museos_accesibles:
    #    print(museo.nombre)
    #    resp += '<li><a href="' + str(museo.contentURL) + '">' + str(museo.nombre) +'</a></li>'
    #resp += "</ol>"

    paginas_users = PaginaUser.objects.all()
    #pag = ""
    #for pagina in paginas_users:
    #    pag += '<li><a href="/' + str(pagina.user.username) + '">' + str(pagina.titulo) +'</a></li>'

    #accesibilidad = '<form action="/" ><button type="submit">Página principal</button></form>'

    context = {'name': request.user.username,'aut': request.user.is_authenticated(),
                'museos_accesibles': museos_accesibles, 'paginas_users': paginas_users}
    return render(request, 'accesibilidad.html', context)
    #return HttpResponse(resp)



def cargarComentario(request):
    if request.user.is_authenticated():
        # if this is a POST request we need to process the form data
        if request.method == 'POST':
            # create a form instance and populate it with data from the request:
            form = nuevoComentario(request.POST)
            # check whether it's valid:
            if form.is_valid():
                nuevo_comentario = Comentario()
                nuevo_comentario.museo = form.cleaned_data['museo']
                nuevo_comentario.texto = form.cleaned_data['comentario']
                user = User.objects.get(username=request.user.username)
                nuevo_comentario.user = user
                #print(form.cleaned_data)
                nuevo_comentario.save()


                return HttpResponseRedirect('/')
            else:
                print("IT IS NOT VALID")

        # if a GET (or any other method) we'll create a blank form
        else:
            form = nuevoComentario()

        context = {'name': request.user.username,'aut': request.user.is_authenticated(),'form': form}
        return render(request, 'comentarios.html', context)

    else:
        resp = ""
        context = {'name': request.user.username,'aut': request.user.is_authenticated(),'respuesta': resp}
        return render(request, 'comentarios.html', context)




def detallesMuseo(request, identificador):
    try:
        museo = Museo.objects.get(id=identificador)
        #resp = museo.nombre
    except ObjectDoesNotExist:
        #resp = "ID inválido"
        context = {'name': request.user.username,'aut': request.user.is_authenticated()}
        return render(request, 'error.html', context)

    comentarios = Comentario.objects.filter(museo__nombre__contains=museo.nombre)
    #if comentarios.count() != 0:
    #    resp += comentarios[0].texto
    #    print("Comentarios: " + comentarios[0].texto)
    #else:
    #    resp += "Museo sin comentarios, ¡se el primero en comentar!"



    if request.user.is_authenticated():
        # if this is a POST request we need to process the form data
        if request.method == 'POST':
            # create a form instance and populate it with data from the request:
            form = nuevoComentario(request.POST)
            # check whether it's valid:
            if form.is_valid():
                nuevo_comentario = Comentario()
                nuevo_comentario.museo = museo
                nuevo_comentario.texto = form.cleaned_data['comentario']
                user = User.objects.get(username=request.user.username)
                nuevo_comentario.user = user
                #print(form.cleaned_data)
                nuevo_comentario.save()


                form = nuevoComentario()
            else:
                print("IT IS NOT VALID")

        # if a GET (or any other method) we'll create a blank form
        else:
            form = nuevoComentario()

        seleccion = Seleccion.objects.filter(user__username__contains=request.user.username).filter(museo__nombre__contains=museo.nombre)
        #museo = Seleccion.objects.get(museo=museo)
        seleccionado = True
        if seleccion.count() == 0:
            print("ESTA VACIO")
            seleccionado = False
            #nueva_seleccion = Seleccion()
            #nueva_seleccion.museo = museo
            #user = User.objects.get(username=request.user.username)
            #nueva_seleccion.user = user
            #nueva_seleccion.save()
        else:
            print("SI ESTA SELECCIONADO")


        #context = {'name': request.user.username,'aut': request.user.is_authenticated(),'form': form}
        #return render(request, 'comentarios.html', context)
    else:
        form = None
        seleccionado = False


    context = {'name': request.user.username,'aut': request.user.is_authenticated(),'museo': museo,
                'comentarios': comentarios, 'form': form, 'id': identificador, 'seleccionado': seleccionado}
    return render(request, 'detalles_museo.html', context)

@csrf_exempt
def gestionSeleccion(request, identificador):

    museo = Museo.objects.get(id=identificador)
    seleccion = Seleccion.objects.filter(user__username__contains=request.user.username).filter(museo__nombre__contains=museo.nombre)
    if seleccion.count() < 1:
        nueva_seleccion = Seleccion()
        nueva_seleccion.museo = museo
        user = User.objects.get(username=request.user.username)
        nueva_seleccion.user = user
        nueva_seleccion.save()
    print("Seleccion")
    return detallesMuseo(request, identificador)

    #return HttpResponse("Hola caracola")

@csrf_exempt
def gestionDeseleccion(request, identificador):

    museo = Museo.objects.get(id=identificador)
    seleccion = Seleccion.objects.filter(user__username__contains=request.user.username).filter(museo__nombre__contains=museo.nombre)
    seleccion.delete()
    print("Deseleccion")
    return detallesMuseo(request, identificador)
    #return HttpResponse("Hola caracola")




def about(request):
    resp = "<br>Autor: Rodrigo Perela Posada</br>"
    resp += "<br>ITT-IAA ETSIT</br>"
    context = {'name': request.user.username,'aut': request.user.is_authenticated(),'respuesta': resp}
    return render(request, 'about.html', context)


def prueba(request):
    context = {'name': request.user.username,'aut': request.user.is_authenticated()}
    return render(request, 'index.html', context)


@csrf_exempt
def museosDistrito(request):
    if request.method == "GET":
        form = filtrarDistrito()
        #distritos = set(Museo.objects.order_by('distrito'))
        #distritos = Museo.objects..unique().values_list('distrito')
        distritos = set(Museo.objects.values_list('distrito',flat=True).order_by('distrito'))
        #print(distritos)
        distritos2 = list(set(Museo.objects.all().values_list('distrito')))
        #print(distritos2)
        museos = Museo.objects.all()
        '''
        resp = ""
        for museo in museos:
            #print(museo.nombre)
            resp += '<li><a href="/museo/' + str(museo.id) + '">' + str(museo.nombre) + '</a></li>'

        '''
        distrito = "Todos"
        #context = {'form': form, 'lista_museos': museos, 'distrito': distrito}
        #return render(request, 'barra_museos.html', context)
    #return HttpResponse(resp)
    elif request.method == "POST":
        #print(form.errors)
        distrito = request.POST.get('distrito')
        print("|" + distrito + "|")
        form = filtrarDistrito()
        if distrito != "":
            print("Mi distrito: " + distrito)
            museos = Museo.objects.filter(distrito=distrito)

            #return HttpResponseRedirect('/thanks/')
            #context = {'form': form, 'lista_museos': museos_filtrados, 'distrito': distrito}
            #return render(request, 'barra_museos.html', context)
        else:
            museos = Museo.objects.all()
            distrito = "Todos"
            #return HttpResponse("Funciona mal!")

    context = {'name': request.user.username,'aut': request.user.is_authenticated(),
                'form': form, 'lista_museos': museos, 'distrito': distrito}
    return render(request, 'barra_museos.html', context)


@csrf_exempt
def loginView(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)

        try:
            pagina_usuario = PaginaUser.objects.get(user=user)
        #print(pagina_usuario.titulo)
        #print(PaginaUser.objects.get(user=username))
        except ObjectDoesNotExist:
            titulo = "Pagina de " + username
            pagina_usuario = PaginaUser(user = user, titulo = titulo)
            pagina_usuario.save()

        return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/')




@csrf_exempt
def barra(request):
    if request.method == "GET":
        count_mess = Museo.objects.annotate(number_of_comments=Count('comentario')).filter(number_of_comments__gte=1).order_by('-number_of_comments')[:5]
        #print("LLEGO HASTA AQUI")
        #aux = number_of_comments.filter()
        #print("Num comentarios primer : " + str(count_mess[0].number_of_comments))
        #print(count_mess)
        #resp = "<p><h2>Museos con más comentarios:</h2></p>"
        print("Numero museos con comentarios: " + str(count_mess.count()))
        if count_mess.count() != 0:
            resp = "<ol>"
            i = 0
            for museo in count_mess:
                print(museo.nombre)
                resp += '<li><a href="' + str(museo.contentURL) + '">' + str(museo.nombre) +'</a>: ' + str(Comentario.objects.filter(museo__nombre__contains=museo.nombre).count()) + ' comentario(s)</br>'
                resp += str(museo.claseVial) + " " + str(museo.nombreVia) + ", " + str(museo.numero) + " " + str(museo.codPostal) + " " + str(museo.localidad) + "</br>"
                resp += "Barrio / Distrito " + str(museo.barrio) + " / " + str(museo.distrito) + "</br>"
                resp += ' <a href="/museos/' + str(museo.id) + '"> (Más información)</a></li></br><hr>'
                i = i + 1
            resp += "</ol>"

        else:
            resp += "No comments yet!</br></br>"

        #resp += '<form method="link" action="/acces/">'
        #resp += '<input type="button" value="Start"></form>'

        #accesibilidad = '<form action="/acces/" ><button type="submit">Museos accesibles</button></form>'

        paginas_users = PaginaUser.objects.all()
        #pag = ""
        #for pagina in paginas_users:
        #    pag += '<li><a href="/' + str(pagina.user.username) + '">' + str(pagina.titulo) +'</a></li>'




        context = {'name': request.user.username,'aut': request.user.is_authenticated(), 'respuesta': resp, 'paginas_users': paginas_users}
        return render(request, 'barra.html', context)
        #return HttpResponse(resp)


def xmlParser(req):
    xmlFile = urlopen(XML_URL)
    tree = ET.parse(xmlFile)
    root = tree.getroot()
    Museo.objects.all().delete()
    for listMuseos in root.iter('contenido'):
        try:
            print("-----------------------------------------")
            for museo in listMuseos.findall('atributos'):
                try:
                    nombre = museo.find('atributo[@nombre="NOMBRE"]').text
                    print (nombre)
                except AttributeError:
                    print ("Campo nombre NO encontrado")
                    pass

                try:
                    descripcion = museo.find('atributo[@nombre="DESCRIPCION-ENTIDAD"]').text
                    print (descripcion)
                except AttributeError:
                    descripcion = " "
                    print ("Campo descripcion NO encontrado")
                    pass

                try:
                    descripcion += museo.find('atributo[@nombre="DESCRIPCION"]').text
                    print (descripcion)
                except AttributeError:
                    print ("Campo descripcion2 NO encontrado")
                    pass

                try:
                    horario = museo.find('atributo[@nombre="HORARIO"]').text
                    print (horario)
                except AttributeError:
                    print ("Campo horario NO encontrado")
                    pass

                try:
                    transporte = museo.find('atributo[@nombre="TRANSPORTE"]').text
                    print (transporte)
                except AttributeError:
                    print ("Campo transporte NO encontrado")
                    pass

                #accesibilidad = int(museo.find('atributo[@nombre="ACCESIBILIDAD"]').text,2)
                if museo.find('atributo[@nombre="ACCESIBILIDAD"]').text == "0":
                    accesibilidad = False
                else:
                    accesibilidad = True
                print (accesibilidad)

                try:
                    contentURL = museo.find('atributo[@nombre="CONTENT-URL"]').text
                    print (contentURL)
                except AttributeError:
                    print ("Campo contentURL NO encontrado")
                    pass


                localizacion = museo.find('atributo[@nombre="LOCALIZACION"]')
                try:
                    nombre_via = localizacion.find('atributo[@nombre="NOMBRE-VIA"]').text
                    print (nombre_via)
                except AttributeError:
                    print ("Campo nombre_via NO encontrado")
                    pass
                try:
                    clase_vial = localizacion.find('atributo[@nombre="CLASE-VIAL"]').text
                    #clase_vial = "(" + clase_vial + ")"
                    print (clase_vial)
                except AttributeError:
                    print ("Campo clase_vial NO encontrado")
                    pass
                try:
                    numero = localizacion.find('atributo[@nombre="NUM"]').text
                    #numero = "NUM " + numero
                    print (numero)
                except AttributeError:
                    print ("Campo numero NO encontrado")
                    pass
                try:
                    localidad = localizacion.find('atributo[@nombre="LOCALIDAD"]').text
                    print (localidad)
                except AttributeError:
                    print ("Campo localidad NO encontrado")
                    pass
                try:
                    cod_postal = localizacion.find('atributo[@nombre="CODIGO-POSTAL"]').text
                    print (cod_postal)
                except AttributeError:
                    print ("Campo cod_postal NO encontrado")
                    pass
                try:
                    barrio = localizacion.find('atributo[@nombre="BARRIO"]').text
                    print (barrio)
                except AttributeError:
                    print ("Campo barrio NO encontrado")
                    pass
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



        museo = Museo(nombre = nombre, descripcion = descripcion, horario = horario, transporte = transporte,
                      accesibilidad = accesibilidad, contentURL = contentURL, nombreVia = nombre_via, claseVial = clase_vial,
                      numero = numero, localidad = localidad, codPostal = cod_postal, barrio = barrio, distrito = distrito,
                      telefono = telefono, email = email)
        print("!!!!!!!!!!!!!!!!!!!!!!!!! Antes de guardar Museo !!!!!!!!!!!!!!!!!!!!!!!!!")
        museo.save()
        print("!!!!!!!!!!!!!!!!!!!!!!!!! Despues de guardar Museo !!!!!!!!!!!!!!!!!!!!!!!!!")
        nombre = descripcion = horario = transporte = accesibilidad = contentURL = None
        nombre_via = clase_vial = numero = localidad = cod_postal = barrio = distrito = telefono = email = None
    #resp = "<a href=/xml>Cargar xml</a>"
    #return HttpResponse(resp)
    return HttpResponseRedirect('/')
