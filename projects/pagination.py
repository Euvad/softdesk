from rest_framework.pagination import PageNumberPagination

class CustomPageNumberPagination(PageNumberPagination):
    page_size = 20  # Default number of items per page
    page_size_query_param = 'page_size'  # Clients can override the page size
    max_page_size = 100  # Maximum items per page to avoid large requests
