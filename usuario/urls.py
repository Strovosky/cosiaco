from django.urls import path
from .views import VistaLogin



urlpatterns = [
    path(route="login/", view=VistaLogin.as_view(), name="login")
]













