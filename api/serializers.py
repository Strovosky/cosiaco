from rest_framework.serializers import ModelSerializer, Serializer, EmailField, CharField, ValidationError
from usuario.models import Usuario
from django.contrib.auth import get_user_model
from los_cosiacos.models import Cosiaco, Categoria, Estrella, Opinion, Like



class UsuarioSerializador(ModelSerializer):
    """Este sera el serializador basico para el Usuario."""
    
    class Meta:
        model = Usuario
        fields = [
            'id',
            'correo',
            'usuario',
            'bio',
            'celular',
            'password'
        ]
        # To only accept a password but not display it.
        extra_kwargs = {
            'password':{"write_only":True}
        }
    
    def create(self, validated_data):
        # We'll make sure to save the password into the instance
        password = validated_data.pop("password")
        instance = self.Meta.model(**validated_data)
        instance.set_password(password)
        instance.save()
        return instance
    
    def update(self, instance, validated_data):
        # Modificaremos la actualización porque no queremos que se actualice ni el correo electronico ni el usuario
        
        try:
            instance.celular = validated_data["celular"]
        except:
            pass
        try:
            instance.bio = validated_data["bio"]
        except:
            pass
        instance.save()
        return instance
    

class UsuarioLoginSerializador(Serializer):

    correo = EmailField(max_length=50, min_length=5, required=True)
    password = CharField(max_length=30, min_length=5, write_only=True, required=True)

    def validate_correo(self, value):
        Usuario = get_user_model()
        if not Usuario.objects.filter(correo=value).exists():
            raise ValidationError("No existe un usuario con este correo")
        return value




class CosiacoSerializador(ModelSerializer):
    """Este será el serializador básico para los cosiacos."""

    class Meta:
        model = Cosiaco
        fields = [
            "id",
            "creador",
            "categoria",
            "nombre",
            "descripcion",
            "fecha_creacion",
            "mostrar_estrellas"
        ]

    def create(self, validated_data):
        """Vamos a modificar el create para que cree el cosiaco con el usuario."""
        request = self.context.get("request")
        categoria = Categoria.objects.get(id=int(request.data.get("categoria")))
        try:
            descripcion = validated_data["descripcion"]
        except:
            cosiaco = request.user.cosiaco_set.create(nombre=validated_data["nombre"])
        else:
            cosiaco = request.user.cosiaco_set.create(nombre=validated_data["nombre"], descripcion=descripcion)
            cosiaco.categoria.add(categoria)
            cosiaco.save()
        return cosiaco


class CategoriaSerializador(ModelSerializer):
    """Este serializador manejara la informacion del modelos Categoria"""

    class Meta:
        model = Categoria
        fields = [
            "id",
            "nombre"
        ]


class EstrellaSerializador(ModelSerializer):
    """Ester serializador manejara la informacion del modelo Estrella"""

    class Meta:
        model = Estrella
        fields = [
            "creador",
            "cosiaco",
            "numero"
        ]


class OpinionSerializador(ModelSerializer):
    """Este serializador manejara la informacion del modelo Opinion"""

    class Meta:
        model = Opinion
        fields = [
            "id",
            "creador",
            "cosiaco",
            "descripcion",
            "fecha_creacion"
        ]


class LikeSerializador(ModelSerializer):
    """
    Este serializador manejará la información del modelo Like
    """

    class Meta:
        model = Like
        fields = [
            "id",
            "creador",
            "opinion"
        ]

