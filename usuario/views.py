from django.shortcuts import render
from django.views import View

# Create your views here.


class VistaLogin(View):
    """
    Esta vista manejará el la página de login.
    """

    def get(self, request, *args, **kwargs):
        return render(request, "usuario/login.html", {})
    
    def post(self, request, *args, **kwargs):
        pass



