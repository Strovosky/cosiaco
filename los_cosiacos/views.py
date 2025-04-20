from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.utils.decorators import method_decorator
from .decorators import usuario_autenticado_redireccion
from django.views import View
import requests
from api.endpoints import verificar_token_usuario, obtener_usuario_class_view

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

    def get(self, request, *args, **kwargs):
        return render(request, "los_cosiacos/browse.html")



class VistaPeril(View):

    def get(self, request, *args, **kwargs):
        respuesta_usuario = requests.get(url=obtener_usuario_class_view, headers={"Authorization":F"Token {request.COOKIES.get("auth_token")}"}, timeout=2)
        if respuesta_usuario.status_code == 200:
            return render(request, "los_cosiacos/perfil.html", {"usuario":respuesta_usuario.json()})
        if respuesta_usuario.status_code == 400:
            for message in respuesta_usuario.json():
                messages.add_message(request, messages.INFO, message.value())
            return HttpResponseRedirect(reverse("usuario_urls:login"))
        if respuesta_usuario.status_code == 404:
            for message in respuesta_usuario.json():
                messages.add_message(request, messages.INFO, message.value())
            return HttpResponseRedirect(reverse("usuario_urls:login"))
    
        for message in respuesta_usuario.json():
            messages.add_message(request, messages.INFO, message.value())
        return HttpResponseRedirect(reverse("usuario_urls:login"))



