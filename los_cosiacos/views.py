from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from .decorators import usuario_autenticado_redireccion
from django.views import View
import requests
from api.endpoints import verificar_token_usuario

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

