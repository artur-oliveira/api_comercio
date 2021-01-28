from django.urls import path, re_path
from rest_framework import permissions

from .views import (CategoriaList, CategoriaDetail,
                    UserList, UserDetail,
                    PagamentoList, PagamentoDetail,
                    ProdutoList, ProdutoDetail,
                    VendaList, VendaDetail,
                    api_root, ProdutoMaisVendido, PagamentoMaisUtilizado)

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Vendas API",
      default_version='v1',
      description="Uma API de controle de estoque e de vendas, para fins de testes haverá dois usuários vendedor "
                  "com as seguintes credenciais:\nVendedor 1:\nusername -> vendedor_01\npassword -> P@ssw0rD\n\n"
                  "Vendedor 2:\nusername -> vendedor_02\npassword -> P@ssw0rD\n\n"
                  "E também dois usuários clientes com as seguintes credenciais:\nCliente 1:\nusername -> cliente_01\n"
                  "password -> P@ssw0rD\n\n"
                  "Cliente 2:\nusername -> cliente_02\npassword -> P@ssw0rd",
      contact=openapi.Contact(email="artur.oliveira9876@gmail.com"),
      license=openapi.License(name="MIT License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('', api_root, name='api-root'),

    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

    path('categoria/', CategoriaList.as_view(), name='categoria'),
    path('categoria/<int:pk>', CategoriaDetail.as_view(), name='categoria-detail'),

    path('pagamento/', PagamentoList.as_view(), name='pagamento'),
    path('pagamento/<int:pk>', PagamentoDetail.as_view(), name='pagamento-detail'),

    path('produto/', ProdutoList.as_view(), name='produto'),
    path('produto/<int:pk>', ProdutoDetail.as_view(), name='produto-detail'),

    path('venda/', VendaList.as_view(), name='venda'),
    path('venda/<int:pk>', VendaDetail.as_view(), name='venda-detail'),

    path('users/', UserList.as_view(), name='user'),
    path('users/<int:pk>', UserDetail.as_view(), name='user-detail'),

    path('stats/produto-mais-vendido', ProdutoMaisVendido.as_view(), name='produto-mais-vendido'),
    path('stats/pagamento-mais-utilizado', PagamentoMaisUtilizado.as_view(), name='pagamento-mais-utilizado')
]
