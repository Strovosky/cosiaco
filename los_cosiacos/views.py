from django.shortcuts import render
from django.views import View

# Create your views here.



class IndexView(View):
    """
    Esta vista mostrará la página index.
    """

    def get(self, request, *args, **kwargs):
        return render(request, "los_cosiacos/index.html", {})


class BrowseView(View):
    """
    Esta vista manejará la pagina de busqueda una vez uno se ha logeado.
    """

    def get(self, request, *args, **kwargs):
        return render(request, "los_cosiacos/browse.html")

