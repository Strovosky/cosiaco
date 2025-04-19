from django.urls import path
from .views import VistaLogin, VistaLogout

app_name = "usuario_urls"

urlpatterns = [
    path(route="login/", view=VistaLogin.as_view(), name="login"),
    path(route="logout/", view=VistaLogout.as_view(), name="logout")
]













