from django.urls import path
from .views import VistaLogin

app_name = "usuario_urls"

urlpatterns = [
    path(route="login/", view=VistaLogin.as_view(), name="login")
]













