from django.shortcuts import redirect
import requests
from api.endpoints import verificar_token_usuario



def usuario_autenticado_redireccion(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.COOKIES.get("auth_token"):
            token_validation = requests.post(url=verificar_token_usuario, headers={"Authorization":f"Token {request.COOKIES.get("auth_token")}"}, timeout=2)
            if token_validation.status_code == 200:
                response = redirect(to=("los_cosiacos_urls:browse"))
                response.set_cookie(key="auth_token", value=request.COOKIES.get("auth_token"))
                return response
        return view_func(request, *args, **kwargs)
    return wrapper_func







