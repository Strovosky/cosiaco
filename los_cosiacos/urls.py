from django.urls import path
from .views import IndexView, BrowseView, VistaPeril
from django.conf import settings
from django.conf.urls.static import static

app_name = "los_cosiacos_urls"

urlpatterns = [
    path(route="", view=IndexView.as_view(), name="index"),
    path(route="browse/", view=BrowseView.as_view(), name="browse"),
    path(route="perfil/", view=VistaPeril.as_view(), name="perfil")
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)





















