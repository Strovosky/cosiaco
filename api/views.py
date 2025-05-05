
# Django Imports
from django.db.models import Q
from django.shortcuts import render, get_object_or_404

# Local Imports
from usuario.models import Usuario
from los_cosiacos.models import Cosiaco, Categoria, Estrella, Opinion, Like
from .pagination import CosiacoPerfilPagination, OpinionCosiacoPagination
from .serializers import (
    UsuarioSerializador,
    CosiacoSerializador,
    CategoriaSerializador,
    EstrellaSerializador,
    OpinionSerializador,
    LikeSerializador,
    UsuarioLoginSerializador,
    UsuarioPerfilSerializador,
    CosiacoSerializadorRelacionados)

# Rest Framework imports
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.authtoken.models import Token
from rest_framework.authentication import authenticate
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.views import APIView
from rest_framework.generics import (
    CreateAPIView,
    RetrieveAPIView,
    ListAPIView,
    UpdateAPIView,
    DestroyAPIView,
    GenericAPIView)
from rest_framework.mixins import (
    DestroyModelMixin,
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    ListModelMixin)


# The API Views

@api_view(["POST"])
def crear_usuario_api_view(request):
    
    usuario_serializado = UsuarioSerializador(data=request.data, many=False)

    if usuario_serializado.is_valid(raise_exception=True):
        usuario_serializado.save()
        return Response(usuario_serializado.data, status=status.HTTP_201_CREATED)
    
    return Response(usuario_serializado.data, status=status.HTTP_400_BAD_REQUEST)


class CrearUsuarioAPIView(APIView):

    def post(self, request):
        usuario_serializado = UsuarioSerializador(data=request.data, many=False)
        if usuario_serializado.is_valid(raise_exception=True):
            usuario_serializado.save()
            return Response(usuario_serializado.data, status=status.HTTP_201_CREATED)
        return Response(usuario_serializado.errors, status=status.HTTP_400_BAD_REQUEST)


class CrearUsuarioGenericAPIView(CreateAPIView):

    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializador



@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes(TokenAuthentication)
def obtener_usuario_api_view(request, pk):

    usuario = get_object_or_404(Usuario, pk=pk)
    usuario_serializado = UsuarioSerializador(usuario, many=False)
    return Response(usuario_serializado.data, status=status.HTTP_200_OK)


class ObtenerUsuarioClassView(APIView):
    """Esta API View dará al usuario actual."""

    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]

    def get(self, request):
        try:
            token_str = request.headers.get("Authorization").split(" ")[-1]
        except:
            return Response({"error_token":"El token no se pasó adecuadamente"}, status=status.HTTP_400_BAD_REQUEST)
        usuario = Token.objects.select_related("user").filter(key=token_str).first().user
        if not usuario:
            return Response({"error_usuario":"No existe usuario con ese token"}, status=status.HTTP_404_NOT_FOUND)
        usuario_serializado = UsuarioSerializador(usuario)
        return Response(usuario_serializado.data, status=status.HTTP_200_OK)


class ObtenerUsuarioGenericView(RetrieveAPIView):

    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializador
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    lookup_field = "pk"
    

class ObtenerUsuarioPerfilAPIView(APIView):
    """
    Este API View brindará la información del usuario para mostrar en el perfil.
    """
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            token_str = request.headers.get("Authorization").split(" ")[-1]
        except:
            return Response({"token error":"There's something wrong with the token"}, status=status.HTTP_400_BAD_REQUEST)
        usuario = Token.objects.select_related("user").filter(key=token_str).first().user
        if usuario:
            usuario_serializado = UsuarioPerfilSerializador(usuario)
            try:
                usuario_serializado.data
                return Response(usuario_serializado.data, status=status.HTTP_200_OK)
            except:
                return Response({"error serializacion":"No se seralizó el usuario correctamente"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"usuario error":"No hay un usuario con ese token"}, status=status.HTTP_404_NOT_FOUND)




@api_view(['GET'])
@permission_classes([IsAdminUser, IsAuthenticated])
@authentication_classes([TokenAuthentication])
def obtener_todos_los_usuarios_api_view(request):

    usuarios = Usuario.objects.filter(is_active=True)
    usuarios_serializados = UsuarioSerializador(usuarios, many=True)
    return Response(usuarios_serializados.data, status=status.HTTP_200_OK)


class ObtenerTodosLosUsuariosAPIView(APIView):

    permission_classes = [IsAuthenticated, IsAdminUser]
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        usuarios_activos = Usuario.objects.filter(is_active=True)
        usuarios_serializados = UsuarioSerializador(usuarios_activos, many=True)
        return Response(usuarios_serializados.data, status=status.HTTP_200_OK)


class ObtenerTodosLosUsuariosGenericView(ListAPIView):

    permission_classes = [IsAuthenticated, IsAdminUser]
    authentication_classes = [TokenAuthentication]

    queryset = Usuario.objects.filter(is_active=True)
    serializer_class = UsuarioSerializador


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def actualizar_partial_usuario_api_view(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    usuario_actualmente_autenticado = Token.objects.get(key=request.headers.get("Authorization").split(" ")[-1]).user
    if usuario.id != usuario_actualmente_autenticado.id:
        return Response({"error usuario autenticado":"El usuario actualmente autenticado y el usuario que busca no son el mismo"}, status=status.HTTP_400_BAD_REQUEST)
    usuario_serializado = UsuarioSerializador(usuario, data=request.data, partial=True, many=False)
    if usuario_serializado.is_valid(raise_exception=True):
        if "usuario" in request.data.keys() or "correo" in request.data.keys():
            return Response({"error de actualización":"El correo o el usuario no se pueden cambiar."}, status=status.HTTP_400_BAD_REQUEST)
        usuario_serializado.save()
        return Response(usuario_serializado.data, status=status.HTTP_200_OK)
    return Response({"error":"ocurrio un error con el usuario."}, status=status.HTTP_400_BAD_REQUEST)


class ActualizarParcialUsuarioClassView(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        usuario = get_object_or_404(Usuario, pk=pk)
        if usuario is None:
            return Response({"error_usuario":f"el usuario con id:{pk} no existe."}, status=status.HTTP_404_NOT_FOUND)
        usuario_actual = Token.objects.get(key=request.headers.get("Authorization").split(" ")[-1]).user
        if usuario != usuario_actual:
            return Response({"error_usuario":"El usuario autenticado y el usuario que busca no son el mismo."}, status=status.HTTP_400_BAD_REQUEST)
        
        data = request.data.copy()
        if not data["bio"] and not data["celular"]:
            return Response({"error información":"No se proveyó ni bio ni celular"}, status=status.HTTP_400_BAD_REQUEST)
        if  not data["bio"]:
            data.pop("bio")
        elif not data["celular"]:
            data.pop("celular")
        usuario_serializado = UsuarioSerializador(usuario, data=data, partial=True)
        if usuario_serializado.is_valid(raise_exception=True):
            if "usuario" in request.data.keys() or "correo" in request.data.keys():
                return Response({"error_de_actualización":"El nombre de usuario o correo electrónico no pueden ser actualizados."}, status=status.HTTP_400_BAD_REQUEST)
            usuario_serializado.save()
            return Response(usuario_serializado.data, status=status.HTTP_200_OK)
        return Response({"error_envio_info":"La información enviada no fue la correcta"}, status=status.HTTP_400_BAD_REQUEST)

    
class ActualizarParcialUsuarioGeneriView(UpdateAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Usuario.objects.filter(is_active=True)
    serializer_class = UsuarioSerializador
    lookup_field = "pk"

    def patch(self, request, *args, **kwargs):
        if "usuario" in request.data.keys() or "correo" in request.data.keys():
            return Response({"error de campos":"Los campos Usuario y Correo no se pueden cambiar."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return self.partial_update(request, *args, **kwargs)

@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def desactivar_usuario_api_view(request, pk):

    usuario = get_object_or_404(Usuario, pk=pk)
    if not usuario.is_active:
        return Response({"error de desactivación":"El usuario ya se encuentraba desactivado"}, status=status.HTTP_400_BAD_REQUEST)
    usuario.is_active = False
    usuario.save()

    usuario_serializado = UsuarioSerializador(usuario, many=False)

    return Response(usuario_serializado.data, status=status.HTTP_200_OK)


class DesactivarUsuarioClassView(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        usuario = get_object_or_404(Usuario, pk=pk)
        if not usuario.is_active:
            return Response({"error de desactivación":"El usuario ya se encuentraba desactivado"}, status=status.HTTP_400_BAD_REQUEST)
        usuario.is_active = False
        usuario.save()
        usuario_serializado = UsuarioSerializador(usuario)
        return Response(usuario_serializado.data, status=status.HTTP_200_OK)


class DesactivarUsuarioGenericView(DestroyModelMixin, GenericAPIView):

    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = Usuario.objects.filter(is_active=True)
    serializer_class = UsuarioSerializador
    lookup_field = "pk"

    def destroy(self, request, pk):
        usuario = self.get_object()
        if not usuario.is_active:
            return Response({"error de desactivación":"El usuario ya se encuentraba desactivado"}, status=status.HTTP_400_BAD_REQUEST)
        usuario.is_active = False
        usuario.save()
        usuario_serializado = UsuarioSerializador(usuario)
        return Response(usuario_serializado.data, status=status.HTTP_200_OK)




@api_view(["POST"])
def login_usuario(request):

    try:
        usuario = Usuario.objects.get(correo=request.data["correo"])
    except:
        return Response({"error":f"No hay un usuario con el correo {request.data["correo"]}"}, status=status.HTTP_404_NOT_FOUND)
    else:
        if usuario.is_active == False:
            return Response({"importante":"El usario esta inactivo. Activelo antes de hacer login"}, status=status.HTTP_403_FORBIDDEN)
        else:
            try:
                request.data["password"]
            except:
                return Response({"password_error":"Debe haber una contraseña para poder autenticar al usuario."}, status=status.HTTP_403_FORBIDDEN)
            else:
                usuario = authenticate(request, correo=request.data["correo"], password=request.data["password"])

                if usuario is None:
                    return Response({"error autorizacion":"Las credenciales no son correctas"}, status=status.HTTP_401_UNAUTHORIZED)
                
                token, created = Token.objects.get_or_create(user=usuario)

                return Response({"token":token.key, "id":usuario.id}, status=status.HTTP_201_CREATED)


class LoginUsuarioClassView(APIView):

    def post(self, request):
        usuario_serializado = UsuarioLoginSerializador(data=request.data)
        if not usuario_serializado.is_valid(raise_exception=True):
            return Response(usuario_serializado.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            usuario = authenticate(request, correo=usuario_serializado._validated_data["correo"], password=usuario_serializado.validated_data["password"])
            if usuario is None:
                return Response(usuario_serializado.errors, status=status.HTTP_401_UNAUTHORIZED)
            token, created = Token.objects.get_or_create(user=usuario)
            return Response({"token":token.key, "id":usuario.id}, status=status.HTTP_200_OK)
        


@api_view(["GET"])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def logout_usuario(request):

    try:
        token = Token.objects.get(key=request.headers["Authorization"].split(" ")[-1])
        token.delete()
    except:
        return Response({"no_token":"The user doesn't have a token"}, status=status.HTTP_404_NOT_FOUND)

    return Response({"success":"The token has been deleted"}, status=status.HTTP_200_OK)


class LogoutClassView(APIView):

    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        try:
            token = Token.objects.get(key=request.headers["Authorization"].split(" ")[-1])
        except:
            return Response({"error token":"El token que se proveyó no existe."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            token.delete()
            return Response({"token destruido":"El usuario cerro cesión exitosamente"}, status=status.HTTP_200_OK) 


class VerificadorTokenYAutenticacion(APIView):
    """
    Esta vista verificará si el token actual es valido y si el usuario esta autenticado.
    """

    def post(self, request, *args, **kwargs):
        try:
            token_str = request.headers["Authorization"].split(" ")[1]
        except:
            return Response({"error header":"El header no se pasó apropiadamente"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            token = Token.objects.select_related("user").filter(key=token_str).first()
            if not token:
                return Response({"token_invalido":"El token no es valido"}, status=status.HTTP_401_UNAUTHORIZED)
            if token.user.is_authenticated:
                return Response({"usuario_valido":"El token es valido y el usuario esta autenticado"}, status=status.HTTP_200_OK)
            return Response({"usuario_error":"El usuario no esta autenticado"}, status=status.HTTP_401_UNAUTHORIZED)
        


##### Cosiaco Views #######

class CrearCosiaco(CreateAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CosiacoSerializador


class DestruirCosiacoGeneric(DestroyAPIView):

    queryset = Cosiaco.objects.all()
    serializer_class = CosiacoSerializador
    lookup_field = "pk"

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


class ObtenerCosiacosUsurioGeneric(ListModelMixin, RetrieveModelMixin, GenericAPIView):
    """
    Esta vista dará los cociacos paginados pertenecientes al usuario autenticado.
    """

    queryset = Cosiaco.objects.all()
    serializer_class = CosiacoSerializador
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = CosiacoPerfilPagination
    lookup_field = "pk"

    def retrieve(self, request, *args, **kwargs):
        """
        Modifiqué retrieve para que obtenga multiples cosiacos con el pk del usuario autenticado.
        """
        usuario = get_object_or_404(Usuario, pk=kwargs.get("pk"))
        if not usuario:
            return Response({"error usuario":"el usuario no existe"}, status=status.HTTP_404_NOT_FOUND)
        cosiacos = Cosiaco.objects.filter(creador=usuario).order_by("id")

        paginador = CosiacoPerfilPagination()
        cosiacos_paginados = paginador.paginate_queryset(cosiacos, request)
        cosiacos_serializados = self.get_serializer(cosiacos_paginados, many=True)
        return paginador.get_paginated_response(cosiacos_serializados.data)

    def get(self, request, *args, **kwargs):
        if kwargs.get("pk") is not None:
            return self.retrieve(request, *args, **kwargs)
        return Response({"error cosiacons con usuario":"No se pudieron obtener los cosiacos de este usuario unicamente"}, status=status.HTTP_400_BAD_REQUEST)


class ObtenerCosiacoGeneric(RetrieveAPIView):

    queryset = Cosiaco.objects.all()
    serializer_class = CosiacoSerializador
    lookup_field = "pk"

    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]


class ObtenerUltimosCosiacos(ListAPIView):
    """
    Este API View entregará los ultimos 10 cosiacos
    """

    queryset = Cosiaco.objects.order_by("fecha_creacion").reverse()[:4]
    serializer_class = CosiacoSerializadorRelacionados

    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]


class CrearCategoriaGeneric(CreateAPIView):

    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializador

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]


class DestruirCategoriaGeneric(DestroyAPIView):

    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializador
    lookup_field = "pk"

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]


class ObtenerCategoriaGeneric(RetrieveAPIView):
    """Esta vista obtendra una categoria"""

    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializador
    lookup_field = "nombre"

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    

class ObtenerTodasCategoriasGeneric(ListAPIView):
    """
    Esta vista me dara todas las categorias creadas hasta el momento
    """

    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializador

    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

class CrearEstrellaGeneric(CreateAPIView):
    """Esta vista creara la estrella que se le de a los cosiacos"""

    queryset = Estrella.objects.all()
    serializer_class = EstrellaSerializador

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


class CrearOpinionGenericView(CreateAPIView):
    """Esta vista ayudará a crear una opinion"""

    queryset = Opinion.objects.all()
    serializer_class = OpinionSerializador

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


class ObtenerOpinionCosiaco(RetrieveModelMixin, GenericAPIView):
    """
    Esta vista dara la lista de opiniones paginadas de un cosiaco en particular
    """

    queryset = Opinion.objects.all()
    serializer_class = OpinionSerializador
    lookup_field = "pk"

    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    pagination_class = OpinionCosiacoPagination

    def retrieve(self, request, *args, **kwargs):
        if not kwargs.get("pk"):
            return Response({"no pk":"no se paso el pk en args en retrive"}, status=status.HTTP_400_BAD_REQUEST)
        opiniones = Opinion.objects.select_related("cosiaco").filter(cosiaco_id=kwargs.get("pk")).order_by("fecha_creacion")
        if opiniones.count() < 1:
            return Response({"no opinion":"El cosiaco aun no tiene opiniones"}, status=status.HTTP_404_NOT_FOUND)
        
        # -- Esto de aca --
        #paginador = OpinionCosiacoPagination()
        #opiniones_paginadas = paginador.paginate_queryset(opiniones, request)
        
        # -- Se puede hacer asi mas facil ---
        opiniones_paginadas = self.paginate_queryset(opiniones)
        
        opiniones_serializadas = self.get_serializer(opiniones_paginadas, many=True)
        return self.get_paginated_response(opiniones_serializadas.data)
    
    def get(self, request, *args, **kwargs):
        """Se va a pasar el pk del cosiaco para encontrar sus comentarios"""
        if kwargs.get("pk"):
            return  self.retrieve(request, *args, **kwargs)
        return Response({"error inesperado":"Ocurrio un error inesperado debido a que no se pasó el pk"}, status=status.HTTP_400_BAD_REQUEST)
                


                



class DestruirOpinionGenericView(DestroyAPIView):
    """ESta vista destruira opiniones"""

    queryset = Opinion.objects.all()
    serializer_class = OpinionSerializador
    lookup_field = "pk"

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


class CrearDestruirLikeGenericView(
    CreateModelMixin,
    DestroyModelMixin,
    GenericAPIView
):
    """
    Esta vista creara y destruira los likes que un usuario le de a un post.
    """
    queryset = Like.objects.all()
    serializer_class = LikeSerializador
    lookup_field = "pk"

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
        

### Vistas Estrellas

class VerificadorUsuarioActualVSUsuarioEstrella(APIView):
    """
    Este API View dara True si el usuario actual ya dio una estrella al cosiaco y False si no.
    """

    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            token = Token.objects.select_related("user").get(key=request.headers.get("Authorization").split(" ")[-1])
        except:
            return Response({"erros token":"No se encontró el token"}, status=status.HTTP_404_NOT_FOUND)
        else:
            cosiaco_id = kwargs.get("cosiaco_id")
            cosiaco = get_object_or_404(Cosiaco, pk=int(cosiaco_id))
            if token.user.id in [estrella.creador.id for estrella in cosiaco.estrella_set.all()]:
                return Response({"answer":True}, status=status.HTTP_200_OK)
            return Response({"answer":False}, status=status.HTTP_200_OK)

        

