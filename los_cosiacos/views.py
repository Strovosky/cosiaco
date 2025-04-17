from django.shortcuts import render
from django.views import View

# Create your views here.



class IndexView(View):
    """
    Esta vista mostrará la página index.
    """

    def get(self, request, *args, **kwargs):
        return render(request, "los_cosiacos/index.html", {})

