from rest_framework.serializers import ModelSerializer
#from usuario.models import Usuario
#from los_cosiacos.models import Cosiaco, Categoria



#class UsuarioSerializador(ModelSerializer):
#    """Este sera el serializador basico para el Usuario."""
    
#    class Meta:
#        model = Usuario
#        fields = [
#            'id',
#            'correo',
#            'usuario',
#            'bio',
#            'celular',
#            'password'
#        ]
        # To only accept a password but not display it.
#        extra_kwargs = {
#            'password':{"write_only":True}
#        }
    
#    def create(self, validated_data):
#        # We'll make sure to save the password into the instance
#        password = validated_data.pop("password")
#        instance = self.Meta.model(**validated_data)
#        instance.set_password(password)
#        instance.save()
#        return instance
    
#    def update(self, instance, validated_data):
        # Modificaremos la actualización porque no queremos que se actualice ni el correo electronico ni el usuario
        
#        try:
#            instance.celular = validated_data["celular"]
#        except:
#            pass
#        try:
#            instance.bio = validated_data["bio"]
#        except:
#            pass
#        instance.save()
#        return instance
    

#class CosiacoSerializador(ModelSerializer):
#    """Este será el serializador básico para los cosiacos."""

#    class Meta:
#        model = Cosiaco
#        fields = [
#            "id",
#            "creador",
#            "nombre",
#            "descripcion",
#            "votos",
#            "mostrar_estrellas"
#        ]

#    def create(self, validated_data):
#        """Vamos a modificar el create para que cree el cosiaco con el usuario."""
#        request = self.context.get("request")
#        try:
#            descripcion = validated_data["descripcion"]
#        except:
#            cosiaco = request.user.cosiaco_set.create(nombre=validated_data["nombre"])
#        else:
#            cosiaco = request.user.cosiaco_set.create(nombre=validated_data["nombre"], descripcion=descripcion)
#        return cosiaco


#class CategoriaSerializador(ModelSerializer):
#    """Este serializador manejara la informacion del modelos Categoria"""

#    class Meta:
#        model = Categoria
#        fields = [
#            "nombre"
#        ]