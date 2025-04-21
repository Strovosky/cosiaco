from django.urls import path
from .views import obtener_usuario_api_view, crear_usuario_api_view, obtener_todos_los_usuarios_api_view, actualizar_partial_usuario_api_view, desactivar_usuario_api_view, login_usuario, logout_usuario
from .views import CrearUsuarioAPIView, ObtenerUsuarioClassView, ObtenerTodosLosUsuariosAPIView, ObtenerTodosLosUsuariosGenericView, ActualizarParcialUsuarioClassView, ActualizarParcialUsuarioGeneriView, DesactivarUsuarioClassView, LoginUsuarioClassView, LogoutClassView, CrearOpinionGenericView, DestruirOpinionGenericView, VerificadorTokenYAutenticacion
from .views import CrearCosiaco
from .views import CrearUsuarioGenericAPIView, ObtenerUsuarioGenericView, DesactivarUsuarioGenericView, DestruirCosiacoGeneric, CrearCategoriaGeneric, DestruirCategoriaGeneric, CrearEstrellaGeneric, ObtenerCategoriaGeneric, ObtenerCosiacoGeneric, CrearDestruirLikeGenericView, ObtenerTodasCategoriasGeneric, ObtenerUsuarioPerfilAPIView, ObtenerUltimosCosiacos
# RestFramework imports



urlpatterns = [
    path(route="obtener_usuario/<int:pk>/", view=obtener_usuario_api_view, name="obtener_usuario"),
    path(route="obtener_usuario_class_view/", view=ObtenerUsuarioClassView.as_view(), name="obtener_usuario_class_view"),
    path(route="obtener_usuario_generic_view/<int:pk>/", view=ObtenerUsuarioGenericView.as_view(), name="obtener_usuario_generic_view"),
    path(route="obtener_usuario_perfil/", view=ObtenerUsuarioPerfilAPIView.as_view(), name="obtener_usuario_perfil"),
    
    path(route="crear_usuario/", view=crear_usuario_api_view, name="crear_usuario"),
    path(route="crear_usuario_class_view/", view=CrearUsuarioAPIView.as_view(), name="crear_usuario_class_view"),
    path(route="crear_usuario_generic_api_view/", view=CrearUsuarioGenericAPIView.as_view(), name="crear_usuario_generi_api_view"),
    path(route="obtener_todos_los_usuarios/", view=obtener_todos_los_usuarios_api_view, name="todos_los_usuarios"),
    path(route="obtener_todos_los_usuarios_class_view/", view=ObtenerTodosLosUsuariosAPIView.as_view(), name="obtener_todos_los_usuarios_class_view"),
    path(route="obtener_todos_los_usuarios_generic_view/", view=ObtenerTodosLosUsuariosGenericView.as_view(), name="obtener_todos_los_usuario_generic_view"),
    path(route="actualizacion_parcial_usuario/<int:pk>/", view=actualizar_partial_usuario_api_view, name="actualizacion_parcial_usuario"),
    path(route="actualizacion_parcial_usuario_class_view/<int:pk>/", view=ActualizarParcialUsuarioClassView.as_view(), name="actualizacion_parcial_usuario_class_view"),
    path(route="actualizacion_parcial_usuario_generic_view/<int:pk>/", view=ActualizarParcialUsuarioGeneriView.as_view(), name="actualizacion_parcial_usuario_generic_view"),
    path(route="desactivar_usuario/<int:pk>/", view=desactivar_usuario_api_view, name="desactivar_usuario"),
    path(route="desactivar_usuario_class_view/<int:pk>/", view=DesactivarUsuarioClassView.as_view(), name="desactivar_usuario_class_view"),
    path(route="desactivar_usuario_generic_view/", view=DesactivarUsuarioGenericView.as_view(), name="desactivar_usuario_generic_view"),

    path(route="login_usuario/", view=login_usuario, name="login_usuario"),
    path(route="login_usuario_class_view/", view=LoginUsuarioClassView.as_view(), name="login_usuario_class_view"),
    path(route="logout_usuario/", view=logout_usuario, name="logout_usuario"),
    path(route="logout_class_view/", view=LogoutClassView.as_view(), name="logout_class_view"),
    path(route="verificar_token_usuario/", view=VerificadorTokenYAutenticacion.as_view(), name="verificar_token_usuario"),

    path(route="crear_cosiaco_generic_view/", view=CrearCosiaco.as_view(), name="crear_cosiaco"),
    path(route="destruir_cosiaco_generic_view/<int:pk>/", view=DestruirCosiacoGeneric.as_view(), name="destruir_cosiaco_generic"),
    path(route="obtener_cosiaco_generic/<int:pk>/", view=ObtenerCosiacoGeneric.as_view(), name="obtener_cosiaco_generic"),
    path(route="obtener_ultimos_cosiacos/", view=ObtenerUltimosCosiacos.as_view(), name="obtener_ultimos_cosiacos"),

    path(route="crear_categoria_generic/", view=CrearCategoriaGeneric.as_view(), name="crear_categoria_generic"),
    path(route="destruir_categoria_generic/<int:pk>/", view=DestruirCategoriaGeneric.as_view(), name="destruir_categoria_generic"),
    path(route="obtener_categoria_generic/<str:nombre>/", view=ObtenerCategoriaGeneric.as_view(), name="obtener_categoria_generic"),
    path(route="obtener_todas_categorias_generic/", view=ObtenerTodasCategoriasGeneric.as_view(), name="obtener_todas_categorias_generic"),

    path(route="crear_estrella_generic/", view=CrearEstrellaGeneric.as_view(), name="crear_estrella_generic"),

    path(route="crear_opinion_generic/", view=CrearOpinionGenericView.as_view(), name="crear_opinion_generic"),
    path(route="destruir_opinion_generic/<int:pk>/", view=DestruirOpinionGenericView.as_view(), name="destruir_opinion_generic"),

    path(route="crear_like_generic/", view=CrearDestruirLikeGenericView.as_view(), name="crear_like_generic"),
    path(route="destruir_like_generic/<int:pk>/", view=CrearDestruirLikeGenericView.as_view(), name="destruir_like_generic"),
]





