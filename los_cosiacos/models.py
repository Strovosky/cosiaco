from django.db.models import Model, CharField, IntegerField, DateTimeField, ForeignKey, ManyToManyField, SET_NULL, CASCADE
from django.utils.translation import gettext_lazy as _

from usuario.models import Usuario




class Categoria(Model):
    """Este modelo servira para crear las categorias, solo el admin deberia crear categorias."""

    nombre = CharField(verbose_name=_("nombre"), max_length=50, unique=True)

    def __str__(self):
        return self.nombre


class Cosiaco(Model):
    "Este será el modelos de los cosiacos"

    creador = ForeignKey(verbose_name=_("creador"), to=Usuario, null=True, on_delete=SET_NULL)
    categoria = ManyToManyField(verbose_name=_("categoria"), to=Categoria)

    nombre = CharField(verbose_name=("nombre"), max_length=50, unique=True)
    descripcion = CharField(verbose_name=_("descripción"), max_length=500, null=True, blank=True)
    fecha_creacion = DateTimeField(verbose_name=_("fecha de creación"), auto_now_add=True)

    def mostrar_estrellas(self):
        try:
            if self.estrella_set.count() > 2:
                return sum([e.numero for e in self.estrella_set.all()]) / self.estrella_set.count()
        except:
            return None

    def __str__(self):
        return self.nombre


class Estrella(Model):
    """Este será el modelo de cuantás estrellas tendra un Cosiaco."""

    opciones_numero = [
        (1,1),
        (2,2),
        (3,3),
        (4,4),
        (5,5)
    ]

    creador = ForeignKey(verbose_name=_("creador"), to=Usuario, null=True, on_delete=SET_NULL)
    cosiaco = ForeignKey(verbose_name="cosiaco", to=Cosiaco, on_delete=CASCADE)

    numero = IntegerField(verbose_name=_("número"), choices=opciones_numero)
    fecha_creacion = DateTimeField(verbose_name=_("fecha de creación"), auto_now_add=True)
    
    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.numero}"


class Opinion(Model):
    """Este será el modelo para las opiniones que den los usuarios de un cosiaco."""

    creador = ForeignKey(verbose_name=_("creador"), to=Usuario, null=True, on_delete=SET_NULL)
    cosiaco = ForeignKey(verbose_name="cosiaco", to=Cosiaco, on_delete=CASCADE)

    descripcion = CharField(verbose_name=_("descripción"), max_length=500)
    fecha_creacion = DateTimeField(verbose_name=_("fecha de creación"), auto_now_add=True)

    def mostrar_likes(self):
        try:
            if self.like_set.count() > 0:
                return self.like_set.count()
        except:
            return 0




class Like(Model):
    """Estos serán los likes que se le den a una opinión"""

    creador = ForeignKey(verbose_name=_("creador"), to=Usuario, null=True, on_delete=SET_NULL)
    opinion = ForeignKey(verbose_name=_("opinion"), to=Opinion, on_delete=CASCADE)

    def __str__(self):
        return self.creador.usuario












