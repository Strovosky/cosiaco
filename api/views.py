from django.shortcuts import render, get_object_or_404
from .serializers import UsuarioSerializador, CosiacoSerializador, CategoriaSerializador, EstrellaSerializador, OpinionSerializador, LikeSerializador
from usuario.models import Usuario
from los_cosiacos.models import Cosiaco, Categoria, Estrella, Opinion, Like
from django.db.models import Q

# Rest Framework imports
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.authtoken.models import Token
from rest_framework.authentication import authenticate
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView

from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView, UpdateAPIView, DestroyAPIView, GenericAPIView
from rest_framework.mixins import DestroyModelMixin, CreateModelMixin

# Create your views here.



@api_view(["POST"])
def crear_usuario_api_view(request):
    
    usuario_serializado = UsuarioSerializador(data=request.data, many=False)

    if usuario_serializado.is_valid(raise_exception=True):
        usuario_serializado.save()
        return Response(usuario_serializado.data, status=status.HTTP_201_CREATED)
    
    return Response(usuario_serializado.data, status=status.HTTP_400_BAD_REQUEST)


class CrearUsuarioAPIView(APIView):

    def post(self, request):
        print("Are you even working?")
        print(request.data.get("correo"))
        if Usuario.objects.filter(correo=request.data.get("correo")).count() > 0:
            return Response({"error_existencia":"El usuario ya existe con ese correo."})
        elif Usuario.objects.filter(correo=request.data.get("usuario")).count() > 0:
            return Response({"error_existencia":"El usuario ya existe con ese usuario."})
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

    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request, pk):
        try:
            usuario = get_object_or_404(Usuario, pk=pk)
        except:
            return Response({"404 error":"No hay un usuario con ese pk."}, status=status.HTTP_404_NOT_FOUND)
        else:
            usuario_serializado = UsuarioSerializador(usuario, many=False)
            return Response(usuario_serializado.data, status=status.HTTP_200_OK)


class ObtenerUsuarioGenericView(RetrieveAPIView):

    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializador
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    lookup_field = "pk"
    

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
        usuario_actual = Token.objects.get(key=request.headers.get("Authorization").split(" ")[-1]).user
        if usuario != usuario_actual:
            return Response({"error_usuario":"El usuario autenticado y el usuario que busca no son el mismo."}, status=status.HTTP_400_BAD_REQUEST)
        usuario_serializado = UsuarioSerializador(usuario, data=request.data, partial=True)
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
        if not request.data["correo"] or not request.data["password"]:
            return Response({"credenciales insuficientes":"Se nececita el correo y contraseña para hacer el login"}, status=status.HTTP_400_BAD_REQUEST)
        usuario = Usuario.objects.filter(Q(correo=request.data.get("correo")) & Q(is_active=False))
        if usuario.count() > 1:
            return Response({"usuario desactivado":"El usuario debe ser activado antes de hacer un login"}, status=status.HTTP_401_UNAUTHORIZED)
        usuario = authenticate(request, correo=request.data.get("correo"), password=request.data.get("password"))
        if usuario is None:
            return Response({"error autorizacion":"Las credenciales no son correctas"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
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
            return Response({"token destruido":"El token fue destruido"}, status=status.HTTP_200_OK) 



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



class ObtenerCosiacoGeneric(RetrieveAPIView):

    queryset = Cosiaco.objects.all()
    serializer_class = CosiacoSerializador
    lookup_field = "pk"

    authentication_classes = [TokenAuthentication]
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
        
