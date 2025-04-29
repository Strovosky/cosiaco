# Django imports
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

# Local imports
from .views import IndexView, BrowseView, VistaPeril, ActualizarPerfil, DetalleCosiaco


app_name = "los_cosiacos_urls"

urlpatterns = [
    path(route="", view=IndexView.as_view(), name="index"),
    path(route="browse/", view=BrowseView.as_view(), name="browse"),
    path(route="perfil/", view=VistaPeril.as_view(), name="perfil"),
    path(route="actualizar_perfil/<int:pk>/", view=ActualizarPerfil.as_view(), name="actualizar_perfil"),
    path(route="detalle_cosiaco/<int:pk>/", view=DetalleCosiaco.as_view(), name="detalle_cosiaco"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)





















