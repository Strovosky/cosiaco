# Standard library imports
import requests

# Django Imports
from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views import View

# Local Imports
from .decorators import usuario_autenticado_redireccion, not_logged_user
from api.endpoints import *


# The Views.

class IndexView(View):
    """
    Esta vista mostrará la página index.
    """

    @method_decorator(usuario_autenticado_redireccion)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        ultimos_cuatro_cosiacos_respuesta = requests.get(url=obtener_ultimos_cosiacos, headers={"Authorization":f"Token {request.COOKIES.get("auth_token")}"}, timeout=2)
        cosiacos_populares_respuesta = requests.get(url=obtener_cosiacos_populares, headers={"Authorization":f"Token {request.COOKIES.get("auth_token")}"}, timeout=2)
        if ultimos_cuatro_cosiacos_respuesta.status_code == 200 and cosiacos_populares_respuesta.status_code == 200:
            return render(request, "los_cosiacos/index.html", {"ultimos_cosiacos":ultimos_cuatro_cosiacos_respuesta.json(), "cosiacos_populares":cosiacos_populares_respuesta.json()})
        elif ultimos_cuatro_cosiacos_respuesta.status_code != 200:
            messages.add_message(request, messages.INFO, ultimos_cuatro_cosiacos_respuesta.json().values())
            return render(request, "los_cosiacos/index.html", {})
        elif cosiacos_populares_respuesta.status_code != 200:
            messages.add_message(request, messages.INFO, cosiacos_populares_respuesta.json().values())
            return render(request, "los_cosiacos/index.html", {})
        return render(request, "los_cosiacos/index.html", {})

class BrowseView(View):
    """
    Esta vista manejará la pagina de busqueda una vez uno se ha logeado.
    """

    @method_decorator(not_logged_user)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


    def get(self, request, *args, **kwargs):
        ultimos_cosiacos = requests.get(url=obtener_ultimos_cosiacos, timeout=2)
        cosiacos_populares = requests.get(url=obtener_cosiacos_populares, timeout=2)
        if ultimos_cosiacos.status_code == 200 and cosiacos_populares.status_code == 200:
            return render(request, "los_cosiacos/browse.html", {"ultimos_cosiacos":ultimos_cosiacos.json(), "cosiacos_populares":cosiacos_populares.json()})
        elif ultimos_cosiacos.status_code != 200:
            messages.add_message(request, messages.INFO, ultimos_cosiacos.json().values())
            return render(request, "los_cosiacos/browse.html", {})
        elif cosiacos_populares.status_code != 200:
            messages.add_message(request, messages.INFO, cosiacos_populares.json().values())
            return render(request, "los_cosiacos/browse.html", {})
        return render(request, "los_cosiacos/browse.html")
    
    def post(self, request, *args, **kwargs):
        ultimos_cosiacos = requests.get(url=obtener_ultimos_cosiacos, timeout=2)
        cosiacos_populares = requests.get(url=obtener_cosiacos_populares, timeout=2)
        if ultimos_cosiacos.status_code != 200:
            for value in ultimos_cosiacos.json().values():
                messages.add_message(request, messages.INFO, value)
            return render(request, "los_cosiacos/browse.html", {"ultimos_cosiacos":[], "cosiacos_populares":[], "cosiaco":[], "cosiacos_busqueda":None})
        if cosiacos_populares.status_code != 200:
            for value in cosiacos_populares.json().values():
                messages.add_message(request, messages.INFO, value)
            return render(request, "los_cosiacos/browse.html", {"ultimos_cosiacos":[], "cosiacos_populares":[], "cosiaco":[], "cosiacos_busqueda":None})
        if ultimos_cosiacos.status_code == 200 and cosiacos_populares.status_code == 200:
            if request.POST.get("buscar_c"):
                cosiaco_respuesta = requests.get(url=obtener_cosiaco_por_nombre + request.POST.get("buscar_c") + "/", headers={"Authorization":f"Token {request.COOKIES.get("auth_token")}"}, timeout=2)
                if cosiaco_respuesta.status_code == 200:
                    if request.POST.get("buscar_c") != "":
                        cosiacos_busqueda = requests.get(url=obtener_cosiaco_por_nombre + request.POST.get("buscar_c") + "/", headers={"Authorization":f"Token {request.COOKIES.get("auth_token")}"}, timeout=2)
                        if cosiacos_busqueda.status_code == 200:
                            return render(request, "los_cosiacos/browse.html", {"ultimos_cosiacos":ultimos_cosiacos.json(), "cosiacos_populares":cosiacos_populares.json(), "cosiaco":cosiaco_respuesta.json(), "cosiacos_busqueda":cosiacos_busqueda.json()})
                        else:
                            for value in cosiacos_busqueda.json().values():
                                messages.add_message(request, messages.INFO, value)
                    return render(request, "los_cosiacos/browse.html", {"ultimos_cosiacos":ultimos_cosiacos.json(), "cosiacos_populares":cosiacos_populares.json(), "cosiaco":cosiaco_respuesta.json()})
                else:
                    for value in cosiaco_respuesta.json().values():
                        messages.add_message(request, messages.INFO, value)
                    return render(request, "los_cosiacos/browse.html", {"ultimos_cosiacos": [], "cosiacos_populares": []})
        return render(request, "los_cosiacos/browse.html", {"ultimos_cosiacos":ultimos_cosiacos.json(), "cosiacos_populares":cosiacos_populares.json(), "cosiaco":[]})

class VistaPeril(View):
    """
    Esta vista manejara el template perfil.html y la logica de este.
    """

    @method_decorator(not_logged_user)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
        

    def get(self, request, *args, **kwargs):
        respuesta_usuario = requests.get(url=obtener_usuario_perfil, headers={"Authorization":F"Token {request.COOKIES.get("auth_token")}"}, timeout=2)
        if respuesta_usuario.status_code == 200:
            token_str = request.COOKIES.get("auth_token")
            categorias = requests.get(url=obtener_todas_categorias_generic, headers={"Authorization":f"Token {token_str}"}, timeout=2)
            respuesta_ultimos_cosiacos = requests.get(url=obtener_ultimos_cosiacos, headers={"Authorization":F"Token {request.COOKIES.get("auth_token")}"}, timeout=2)
            respuesta_cosiacos_usuario = requests.get(url=obtener_cosiacos_usuario_generic + f"{respuesta_usuario.json()["id"]}/", headers={"Authorization":f"Token {token_str}"}, timeout=2)
            if respuesta_ultimos_cosiacos.status_code == 200 and respuesta_cosiacos_usuario.status_code == 200:
                return render(request, "los_cosiacos/perfil.html", {"usuario":respuesta_usuario.json(), "categorias":categorias.json(), "ultimos_cosiacos":respuesta_ultimos_cosiacos.json(), "cosiacos":respuesta_cosiacos_usuario.json()})
            else:
                if respuesta_ultimos_cosiacos.status_code != 200:
                    messages.add_message(request, messages.INFO, respuesta_ultimos_cosiacos.json().values())
                    return render(request, "los_cosiacos/perfil.html", {"usuario":respuesta_usuario.json(), "categorias":categorias.json(), "ultimos_cosiacos":{"cosiaco":"no información"}})
                elif respuesta_cosiacos_usuario.status_code != 200:
                    messages.add_message(request, messages.INFO, respuesta_cosiacos_usuario.json().values())
                    return render(request, "los_cosiacos/perfil.html", {"usuario":respuesta_usuario.json(), "categorias":categorias.json(), "ultimos_cosiacos":{"cosiaco":"no información"}})
        if respuesta_usuario.status_code == 400:
            for message in respuesta_usuario.json():
                messages.add_message(request, messages.INFO, message.value())
            return HttpResponseRedirect(reverse("usuario_urls:login"))
        if respuesta_usuario.status_code == 404:
            for message in respuesta_usuario.json():
                messages.add_message(request, messages.INFO, message.value())
            return HttpResponseRedirect(reverse("usuario_urls:login"))
    
        for key, value in respuesta_usuario.json().items():
            messages.add_message(request, messages.INFO, value)
        return HttpResponseRedirect(reverse("usuario_urls:login"))


    def post(self, request, *args, **kwargs):
        if request.POST.get("crear_cosiaco"):
            respuesta_usuario = requests.get(url=obtener_usuario_class_view, headers={"Authorization":F"Token {request.COOKIES.get("auth_token")}"}, timeout=2)
            data = {"creador":respuesta_usuario.json()["id"]}
            for key, value in request.POST.items():
                data.update({key:value})
            respuesta_cosiaco = requests.post(url=crear_cosiaco_generic, headers={"Authorization":f"Token {request.COOKIES.get("auth_token")}"}, data=data, timeout=2)
            if respuesta_cosiaco.status_code == 201:
                messages.add_message(request, messages.INFO, f"El Cosiaco {respuesta_cosiaco.json()["nombre"]} ha sido creado.")
                response = HttpResponseRedirect(reverse("los_cosiacos_urls:perfil"))
                response.set_cookie(key="auth_token", value=request.COOKIES.get("auth_token"), httponly=True)
                return response
            for key, value in respuesta_cosiaco.json().items():
                messages.add_message(request, messages.INFO, value)
            response = HttpResponseRedirect(reverse("los_cosiacos_urls:perfil"))
            response.set_cookie(key="auth_token", value=request.COOKIES.get("auth_token"), httponly=True)
            return response    
        elif request.POST.get("ver_mas") or request.POST.get("ver_anterior"):
            if request.POST.get("ver_mas") is not None:
                url = request.POST.get("ver_mas")
            else:
                url = request.POST.get("ver_anterior")
            respuesta_usuario = requests.get(url=obtener_usuario_perfil, headers={"Authorization":F"Token {request.COOKIES.get("auth_token")}"}, timeout=2)
            respuesta_cosiaco_usuario = requests.get(url=url, headers={"Authorization":F"Token {request.COOKIES.get("auth_token")}"}, timeout=2)
            if respuesta_usuario.status_code != 200:
                messages.add_message(request, messages.INFO, respuesta_usuario.json().values())
                response = HttpResponseRedirect(reverse("los_cosiacos_urls:perfil"))
                response.set_cookie(key="auth_token", value=request.COOKIES.get("auth_token"), httponly=True)
                return response
            if respuesta_cosiaco_usuario.status_code != 200:
                messages.add_message(request, messages.INFO, respuesta_cosiaco_usuario.json().values())
                response = HttpResponseRedirect(reverse("los_cosiacos_urls:perfil"))
                response.set_cookie(key="auth_token", value=request.COOKIES.get("auth_token"), httponly=True)
                return response
            categorias = requests.get(url=obtener_todas_categorias_generic, headers={"Authorization":f"Token {request.COOKIES.get("auth_token")}"}, timeout=2)
            respuesta_ultimos_cosiacos = requests.get(url=obtener_ultimos_cosiacos, headers={"Authorization":F"Token {request.COOKIES.get("auth_token")}"}, timeout=2)
            return render(request, "los_cosiacos/perfil.html", {"usuario":respuesta_usuario.json(), "categorias":categorias.json(), "ultimos_cosiacos":respuesta_ultimos_cosiacos.json(), "cosiacos":respuesta_cosiaco_usuario.json()})
        for key, value in respuesta_usuario.json().items():
            messages.add_message(request, messages.INFO, value)
        response = HttpResponseRedirect(reverse("los_cosiacos_urls:perfil"))
        response.set_cookie(key="auth_token", value=request.COOKIES.get("auth_token"), httponly=True)
        return response

class ActualizarPerfil(View):
    """
    Esta sera la vista que actualizara el perfil del usuario.
    """
    @method_decorator(not_logged_user)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        respuesta_usuario = requests.get(url=obtener_usuario_perfil, headers={"Authorization":f"Token {request.COOKIES.get("auth_token")}"}, timeout=2)
        if respuesta_usuario.status_code != 200:
            for value in respuesta_usuario.json().values():
                messages.add_message(request, messages.INFO, value)
        #respuesta = HttpResponseRedirect(reverse("los_cosiacos_urls:actualizar_perfil", args=((kwargs.get("pk"),))))
        respuesta_ultimos_cosiacos = requests.get(url=obtener_ultimos_cosiacos, headers={"Authorization":F"Token {request.COOKIES.get("auth_token")}"}, timeout=2)
        respuesta = render(request, "los_cosiacos/actualizar_perfil.html", {"usuario":respuesta_usuario.json(), "ultimos_cosiacos":respuesta_ultimos_cosiacos.json()})
        respuesta.set_cookie("auth_token", value=request.COOKIES.get("auth_token"))
        return respuesta

    def post(self, request, *args, **kwargs):
        if request.POST.get("btn_editar_perfil") == "pressed":
            data = request.POST
            respuesta_usuario = requests.patch(url=actualizacion_parcial_usuario_class_view + str(kwargs.get("pk")) + "/", headers={"Authorization":f"Token {request.COOKIES.get("auth_token")}"}, data=data, timeout=2)
            if respuesta_usuario.status_code != 200:
                for value in respuesta_usuario.json().values():
                    messages.add_message(request, messages.INFO, value)
                respuesta = HttpResponseRedirect(reverse("los_cosiacos_urls:actualizar_perfil", args=((kwargs.get("pk"),))))
            else:
                respuesta = HttpResponseRedirect(reverse("los_cosiacos_urls:perfil"))
            respuesta.set_cookie("auth_token", value=request.COOKIES.get("auth_token"))
            return respuesta
        messages.add_message(request, messages.INFO, respuesta_usuario.json().values())
        respuesta = HttpResponseRedirect(reverse("los_cosiacos_urls:actualizar_perfil", args=(kwargs.get("pk"),)))
        respuesta.set_cookie("auth_token", value=request.COOKIES.get("auth_token"))
        return respuesta

class DetalleCosiaco(View):
    """
    Esta vista manejara el template detalle_cosiaco.html y mostrara la infromación de un cosiaco en especifico.
    """

    @method_decorator(not_logged_user)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        cosiaco_respuesta = requests.get(url=obtener_cosiaco_generic + str(kwargs.get("pk")) + "/", headers={"Authorization":f"Token {request.COOKIES.get("auth_token")}"}, timeout=2)
        if cosiaco_respuesta.status_code != 200:
            for value in cosiaco_respuesta.json().values():
                messages.add_message(request, messages.INFO, value)
                respuesta = render(request, "los_cosiacos/detalle_cosiaco.html", {})
        else:
            comentarios_respuesta = requests.get(url=obtener_opinion_cosiaco_generic + str(cosiaco_respuesta.json()["id"]) + "/", headers={"Authorization":f"Token {request.COOKIES.get("auth_token")}"}, timeout=2)
            if comentarios_respuesta.status_code == 200:
                respuesta = render(request, "los_cosiacos/detalle_cosiaco.html", {"cosiaco":cosiaco_respuesta.json(), "comentarios":comentarios_respuesta.json()})
            elif comentarios_respuesta.status_code == 404:
                respuesta = render(request, "los_cosiacos/detalle_cosiaco.html", {"cosiaco":cosiaco_respuesta.json(), "comentarios":None})
            else:
                for value in comentarios_respuesta.json().values():
                    messages.add_message(request, messages.INFO, value)
                    respuesta = render(request, "los_cosiacos/detalle_cosiaco.html", {})
        respuesta.set_cookie("auth_token", request.COOKIES.get("auth_token"), httponly=True)
        return respuesta
    
    def post(self, request, *args, **kwargs):
        cosiaco_respuesta = requests.get(url=obtener_cosiaco_generic + str(kwargs.get("pk")) + "/", headers={"Authorization":f"Token {request.COOKIES.get("auth_token")}"}, timeout=2)
        session_user = requests.get(url=obtener_usuario_perfil, headers={"Authorization":f"Token {request.COOKIES.get("auth_token")}"}, timeout=2)
        if session_user.status_code != 200:
            messages.add_message(request, messages.INFO, session_user.json().values())
            respuesta = HttpResponseRedirect(reverse("los_cosiacos_urls:detalle_cosiaco", args=(cosiaco_respuesta.json()["id"],)))
        elif cosiaco_respuesta.status_code != 200:
            for value in cosiaco_respuesta.json().values():
                messages.add_message(request, messages.INFO, value)
                respuesta = render(request, "los_cosiacos/detalle_cosiaco.html", {})
        else:
            if request.POST.get("btn_estrellas"):
                verificar_usuario_en_estrella = requests.get(url=verificar_usuario_actual_usuario_estrella + str(cosiaco_respuesta.json()["id"]) + "/", headers={"Authorization":f"Token {request.COOKIES.get("auth_token")}"}, timeout=2)
                if verificar_usuario_en_estrella.status_code == 200:
                    if verificar_usuario_en_estrella.json()["answer"] == True:
                        messages.add_message(request, messages.INFO, "No se puede calificar estrellas de un cosiaco mas de una vez.")
                        respuesta = HttpResponseRedirect(reverse("los_cosiacos_urls:detalle_cosiaco", args=(cosiaco_respuesta.json()["id"],)))
                    elif verificar_usuario_en_estrella.json()["answer"] == False:
                        estrella_respuesta = requests.post(url=crear_estrella_generic, headers={"Authorization":f"Token {request.COOKIES.get("auth_token")}"}, data={"creador":session_user.json()["id"], "cosiaco":cosiaco_respuesta.json()["id"], "numero":request.POST.get("estrellas")}, timeout=2)
                        if estrella_respuesta.status_code == 201:
                            messages.add_message(request, messages.INFO, f"Se ha calificado el cosiaco {cosiaco_respuesta.json()["nombre"]} con {request.POST.get("estrellas")} estrellas.")
                        else:
                            for value in estrella_respuesta.json().values():
                                messages.add_message(request, messages.INFO, value)
            if request.POST.get("ver_mas_comentarios"):
                comentarios_respuesta = requests.get(url=request.POST.get("ver_mas_comentarios"), headers={"Authorization":f"Token {request.COOKIES.get("auth_token")}"}, timeout=2)
            elif request.POST.get("ver_comentarios_anteriores"):
                comentarios_respuesta = requests.get(url=request.POST.get("ver_comentarios_anteriores"), headers={"Authorization":f"Token {request.COOKIES.get("auth_token")}"}, timeout=2)
            else:
                if request.POST.get("btn_dejar_comentario") == "pressed":
                    crear_comentario_respuesta = requests.post(url=crear_opinion_generic, headers={"Authorization":f"Token {request.COOKIES.get("auth_token")}"}, data={"creador":session_user.json()["id"], "cosiaco":cosiaco_respuesta.json()["id"], "descripcion":request.POST.get("comentario")}, timeout=2)
                    if crear_comentario_respuesta.status_code != 201:
                        for value in crear_comentario_respuesta.json():
                            messages.add_message(request, messages.INFO, value)
                    else:
                        messages.add_message(request, messages.INFO, f"Se ha dejado un comentario en el cosiaco")
                comentarios_respuesta = requests.get(url=obtener_opinion_cosiaco_generic + str(cosiaco_respuesta.json()["id"]) + "/", headers={"Authorization":f"Token {request.COOKIES.get("auth_token")}"}, timeout=2)
                if comentarios_respuesta.status_code != 200:
                    for value in comentarios_respuesta.json().values():
                        messages.add_message(request, messages.INFO, value)
                    respuesta = render(request, "los_cosiacos/detalle_cosiaco.html", {"cosiaco":cosiaco_respuesta.json(), "comentarios":None})
            respuesta = render(request, "los_cosiacos/detalle_cosiaco.html", {"cosiaco":cosiaco_respuesta.json(), "comentarios":comentarios_respuesta.json()})
        respuesta.set_cookie("auth_token", request.COOKIES.get("auth_token"), httponly=True)
        return respuesta



