from django.urls import path
from .views import IndexView
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path(route="", view=IndexView.as_view(), name="index")
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)





















