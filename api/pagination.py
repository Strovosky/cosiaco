from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination



class CosiacoPerfilPagination(PageNumberPagination):
    """
    Este formato de paginación lo usaré para mostrar solo 8 cosiacos en la pagina de perfil.
    """

    page_size = 8
    page_size_query_param = 'page_size'
    max_page_size = 8


class OpinionCosiacoPagination(PageNumberPagination):
    """
    Este formato de paginación lo usaré para mostrar solo los tres primero comentarios a la vez
    """

    page_size = 3
    page_size_query_param = "page_size"
    max_page_size = 100




