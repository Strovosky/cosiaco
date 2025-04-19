from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.views import View
import requests
from api.endpoints import login_usuario_class_view, crear_usuario_class_view, logout_class_view

# Create your views here.


class VistaLogin(View):
    """
    Esta vista manejará el la página de login.
    """

    def get(self, request, *args, **kwargs):
        return render(request, "usuario/login.html", {})
    
    def post(self, request, *args, **kwargs):
        if request.POST.get("btn_login"):
            usuario_respuesta = requests.post(url=login_usuario_class_view, data=request.POST, timeout=2)
            if usuario_respuesta.status_code == 401 or usuario_respuesta.status_code == 400:
                messages.add_message(request, messages.INFO, "El usuario o contraseña son incorrectos.")
                return render(request, "usuario/login.html", {})
            elif usuario_respuesta.status_code == 200:
                response = HttpResponseRedirect(reverse("los_cosiacos_urls:browse"))
                response.set_cookie("auth_token", usuario_respuesta.json()["token"], httponly=True)
                return response
            messages.add_message(request, messages.INFO, "Ocurrio un error inesperado.")
            return render(request, "usuario/login.html", {})
            
        

class VistaLogout(View):
    """
    Esta vista hara el logout y redireccionara a index.html
    """

    def get(self, request, *args, **kwargs):
        headers = {"Authorization":f"Token {request.COOKIES.get("auth_token")}"}
        logout_response = requests.get(url=logout_class_view, headers=headers, timeout=2)
        if logout_response.status_code == 400:
            for key, value in logout_response.json().items():
                messages.add_message(request, messages.INFO, value)
        if logout_response.status_code == 200:
            for key, value in logout_response.json().items():
                messages.add_message(request, messages.INFO, value)
        response = HttpResponseRedirect(reverse("los_cosiacos_urls:index"))
        response.delete_cookie("auth_token")
        return response







