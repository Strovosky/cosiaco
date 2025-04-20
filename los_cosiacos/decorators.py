from django.shortcuts import redirect
import requests
from api.endpoints import verificar_token_usuario
from django.contrib import messages



def usuario_autenticado_redireccion(view_func):
    """
    Este decorador redireccionara al usuario a browse si ya se encuentra autenticado.
    """
    def wrapper_func(request, *args, **kwargs):
        if request.COOKIES.get("auth_token"):
            token_validation = requests.post(url=verificar_token_usuario, headers={"Authorization":f"Token {request.COOKIES.get("auth_token")}"}, timeout=2)
            if token_validation.status_code == 200:
                response = redirect(to=("los_cosiacos_urls:browse"))
                response.set_cookie(key="auth_token", value=request.COOKIES.get("auth_token"))
                return response
        return view_func(request, *args, **kwargs)
    return wrapper_func



def not_logged_user(view_func):
    """
    Este decorador enviara al usuario a login para que ingrese sus credenciales si ententa ingresar a una pagina sin autorización
    """
    def wrapper_func(request, *args, **kwargs):
        if request.COOKIES.get("auth_token"):
            token_validation = requests.post(url=verificar_token_usuario, headers={"Authorization":f"Token {request.COOKIES.get("auth_token")}"}, timeout=2)
            if token_validation.status_code == 200:
                return view_func(request, *args, **kwargs)
        messages.add_message(request, messages.INFO, "Debe iniciar seción primero antes de entrar a la página anterior.")
        return redirect(to=("usuario_urls:login"))
    return wrapper_func




