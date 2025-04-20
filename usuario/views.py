from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.views import View
import requests
from api.endpoints import login_usuario_class_view, crear_usuario_class_view, logout_class_view, crear_usuario
from los_cosiacos.decorators import usuario_autenticado_redireccion
from django.utils.decorators import method_decorator

# Create your views here.


class VistaLogin(View):
    """
    Esta vista manejará el la página de login.
    """

    @method_decorator(usuario_autenticado_redireccion)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

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


class VistaRegistroUsuario(View):
    """
    Esta vista creará un nuevo usuario.
    """

    @method_decorator(usuario_autenticado_redireccion)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        return render(request, "usuario/registro.html", {})

    def post(self, request, *args, **kwargs):
        usuario_respuesta = requests.post(url=crear_usuario_class_view, data=request.POST, timeout=2)
        if usuario_respuesta.status_code == 201:
            print(usuario_respuesta.json())
            usuario_respuesta_auten = requests.post(url=login_usuario_class_view, data={"correo":usuario_respuesta.json()["correo"], "password":request.POST.get("password")}, timeout=2)
            (usuario_respuesta_auten.json())
            respuesta = HttpResponseRedirect(reverse("los_cosiacos_urls:browse"))
            respuesta.set_cookie(key="auth_token", value=usuario_respuesta_auten.json()["token"], httponly=True)
            return respuesta
        print(usuario_respuesta.json())
        for key, value in usuario_respuesta.json().items():
            messages.add_message(request, messages.INFO, value[0].capitalize())
        return HttpResponseRedirect(reverse("usuario_urls:registro"))






