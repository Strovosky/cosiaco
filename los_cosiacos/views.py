from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.utils.decorators import method_decorator
from .decorators import usuario_autenticado_redireccion, not_logged_user
from django.views import View
import requests
from api.endpoints import verificar_token_usuario, obtener_usuario_class_view, obtener_todas_categorias_generic, crear_cosiaco_generic, obtener_usuario_perfil, obtener_ultimos_cosiacos, obtener_cosiacos_usuario_generic

# Create your views here.


class IndexView(View):
    """
    Esta vista mostrará la página index.
    """

    @method_decorator(usuario_autenticado_redireccion)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, "los_cosiacos/index.html", {})


class BrowseView(View):
    """
    Esta vista manejará la pagina de busqueda una vez uno se ha logeado.
    """

    @method_decorator(not_logged_user)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


    def get(self, request, *args, **kwargs):
        return render(request, "los_cosiacos/browse.html")



class VistaPeril(View):

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



