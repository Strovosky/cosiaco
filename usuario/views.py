from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.views import View
import requests
from api.endpoints import login_usuario_class_view, crear_usuario_class_view

# Create your views here.


class VistaLogin(View):
    """
    Esta vista manejará el la página de login.
    """

    def get(self, request, *args, **kwargs):
        return render(request, "usuario/login.html", {})
    
    def post(self, request, *args, **kwargs):
        try:
            request.POST.get("btn_login")
            print("botón login se activó")
            usuario_respuesta = requests.post(url=login_usuario_class_view, data={"correo":request.POST.get("login_correo"), "password":request.POST.get("login_contraseña")}, timeout=2)
            try:
                usuario_respuesta.json()["error autorizacion"]
                messages.add_message(request, messages.INFO, "El usuario o contraseña son incorrectos.")
                return render(request, "usuario/login.html", {})
            except:
                response = HttpResponseRedirect(reverse("los_cosiacos_urls:browse"))
                response.set_cookie("auth_token", usuario_respuesta.json()["token"], httponly=True)
                return response
        except:
            try:
                request.POST.get("btn_registro")
                print("boton registro funcionó")
                #usuario_respuesta = request.post(url=crear_usuario_class_view, data={"usuario":request.POST.get("registro_usuario"), "correo":request.POST.get("registro_correo"), "password":request.POST.get("registro_contraseña")}, timeout=2)
                print("crear usuario funciono")
                #if usuario_respuesta.json()["error_existencia"]:
                #    messages.add_message(request, messages.INFO, usuario_respuesta.json()["error_existencia"])
                #    return render(request, "usuario/login.html")
                #print(usuario_respuesta.json())
                #usuario_login_respuesta = requests.post(url=login_usuario_class_view, data={"correo":usuario_respuesta.json()["correo"], "password":request.data.get("registro_contraseña")}, timeout=2)
                response = HttpResponseRedirect(reverse("los_cosiacos_urls:browse"))
                #response.set_cookie("auth_token", usuario_login_respuesta.data["token"], httponly=True)
                return response
            except:
                print("error handling worked")
                return render(request, "usuario/login.html", {"error_msm":"Hay un error con la infomración suministrada."})









