# Django importaciones
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator

# Restframework importaciones
from rest_framework.serializers import ModelSerializer, Serializer, EmailField, CharField, ValidationError, SerializerMethodField, HyperlinkedIdentityField

# Local importaciones
from usuario.models import Usuario # Esta la puedo cambiar por get_user_model
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


class UsuarioPerfilSerializador(ModelSerializer):

    num_cosiacos = SerializerMethodField(read_only=True)
    num_comentarios = SerializerMethodField(read_only=True)
    cosiacos_lista = SerializerMethodField(read_only=True)

    class Meta:
        model = get_user_model()
        fields = [
            "id",
            "usuario",
            "correo",
            "bio",
            "celular",
            "cosiacos_lista",
            "num_cosiacos",
            "num_comentarios"
        ]

    def get_num_cosiacos(self, obj):
        return obj.cosiaco_set.count()
    
    def get_num_comentarios(self, obj):
        return obj.opinion_set.count()
    
    def get_cosiacos_lista(self, obj):
        return [{"nombre":cosiaco.nombre} for cosiaco in obj.cosiaco_set.all()]



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


class CosiacoEstrellaUsuario(ModelSerializer):
    """Este Serializador mostrará todos los usuarios de las estrellas de un cosiaco."""

    usuarios_estrellas = SerializerMethodField(read_only=True)

    class Meta:
        model = Cosiaco
        fields = [
            "id",
            "usuarios_estrellas"
        ]
    
    def get_usuario_estrellas(self, obj):
        return {f"usuario{estrella.creador.id}":estrella.creador.id for estrella in obj.estrella_set.all()}


class CosiacoSerializadorRelacionados(ModelSerializer):
    """
    Este serializador muestra la información del cosiaco y sus relacionados
    """
    obtener_cosiaco_url = HyperlinkedIdentityField(view_name="obtener_cosiaco_generic", lookup_field="pk")
    destruir_cosiaco_url = HyperlinkedIdentityField(view_name="destruir_cosiaco_generic", lookup_field="pk")
    categoria = SerializerMethodField(read_only=True)
    creador = SerializerMethodField(read_only=True)
    fecha_creacion = SerializerMethodField(read_only=True)

    class Meta:
        model = Cosiaco
        fields = [
            "id",
            "creador",
            "categoria",
            "nombre",
            "descripcion",
            "fecha_creacion",
            "mostrar_estrellas",
            "obtener_cosiaco_url",
            "destruir_cosiaco_url"
        ]

    def get_categoria(self, obj):
        return [{"nombre":cate.nombre} for cate in obj.categoria.all()]

    def get_creador(self, obj):
        usuario = obj.creador
        return {"usuario":usuario.usuario, "correo":usuario.correo, "bio":usuario.bio, "celular":usuario.celular}
    
    def get_fecha_creacion(self, obj):
        return f"{obj.fecha_creacion.month}/{obj.fecha_creacion.day}/{obj.fecha_creacion.year}"
    


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

    creador = SerializerMethodField(read_only=True)
    fecha_creacion = SerializerMethodField(read_only=True)

    class Meta:
        model = Opinion
        fields = [
            "id",
            "creador",
            "cosiaco",
            "descripcion",
            "fecha_creacion"
        ]
    
    def get_creador(self, obj):
        # Vamos a mostrar el nombre del usuario.
        return obj.creador.usuario
    
    def get_fecha_creacion(self, obj):
        # Vamos a mostar la fecha de creación en un formato mas humano.
        return f"{obj.fecha_creacion.day}/{obj.fecha_creacion.month}/{obj.fecha_creacion.year}"


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

