from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework_simplejwt.serializers import (TokenObtainPairSerializer,
                                                  TokenVerifySerializer,
                                                  TokenRefreshSerializer)
from django.db.models import Q, Count
from .models import (Categoria,
                     User,
                     Pagamento,
                     Produto,
                     Venda,
                     ProdutoVenda,
                     )
from .serializers import (CategoriaSerializer,
                          UserSerializer,
                          PagamentoSerializer,
                          ProdutoSerializer,
                          VendaSerializer,
                          ProdutoMaisVendidoSerializer,
                          PagamentoMaisUtilizadoSerializer,
                          )
from .permissions import (IsSellerOrReadOnly,
                          IsSeller,
                          IsSellerOrClient)

from rest_framework.filters import OrderingFilter
from rest_framework_simplejwt.views import TokenViewBase
from rest_framework.generics import (ListCreateAPIView,
                                     ListAPIView,
                                     RetrieveUpdateDestroyAPIView,
                                     RetrieveAPIView)


class ObterJWTToken(TokenViewBase):
    """
    Com base nas credenciais de usuário, retorna um acessToken e um refreshToken
    O acessToken serve para realizar as requisições que necessitem de autenticação
    O refreshToken serve para gerar um novo acessToken quando este for expirado
    """
    serializer_class = TokenObtainPairSerializer


class RefreshJWTToken(TokenViewBase):
    """
    Gera um novo acessToken com base no refreshToken
    """
    serializer_class = TokenRefreshSerializer


class VerificarToken(TokenViewBase):
    """
    Dado um token, verifica se ele é válido ou não
    """
    serializer_class = TokenVerifySerializer


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'categorias': reverse('categoria', request=request, format=format),
        'pagamentos': reverse('pagamento', request=request, format=format),
        'produtos': reverse('produto', request=request, format=format),
        'vendas': reverse('venda', request=request, format=format),
        'usuarios': reverse('user', request=request, format=format),
    })


class UserList(ListAPIView):
    """
    Lista todos os usuários no sistema, apenas vendedores podem utilizar isso
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsSeller, )


class UserDetail(RetrieveAPIView):
    """
    Detalhes do usuário
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsSeller, )


class CategoriaList(ListCreateAPIView):
    """
    Lista todas as categorias existentes.\n
    Pode ser filtrada por nome, sendo ele exato, ou nomes que contenham a palavra a ser procurar\n
    Pode ser ordenada por id e nome\n
    """
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = (IsSellerOrReadOnly, )

    filter_backends = (DjangoFilterBackend, OrderingFilter,)

    filterset_fields = {'nome': ['icontains', 'exact'], }
    ordering_fields = ('id', 'nome',)


class CategoriaDetail(RetrieveUpdateDestroyAPIView):
    """
    Detalhes da categoria
    """
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = (IsSellerOrReadOnly, )


class PagamentoList(ListCreateAPIView):
    """
    Lista todos os pagamentos existentes.\n
    Pode ser filtrada por nome, sendo ele exato, ou nomes que contenham a palavra a ser procurar\n
    Pode ser filtrada por juros, sendo ele exato, maior, maior ou igual, menor ou menor ou igual\n
    Pode ser ordenada por id, nome e juros\n
    """
    queryset = Pagamento.objects.all()
    serializer_class = PagamentoSerializer
    permission_classes = (IsSellerOrReadOnly, )

    filter_backends = (DjangoFilterBackend, OrderingFilter,)

    filterset_fields = {'nome': ['icontains', 'exact'], 'juros': ['exact', 'lt', 'gt', 'lte', 'gte'], }
    ordering_fields = ('id', 'nome', 'juros',)


class PagamentoDetail(RetrieveUpdateDestroyAPIView):
    """
    Detalhes do pagamento
    """
    queryset = Pagamento.objects.all()
    serializer_class = PagamentoSerializer
    permission_classes = (IsSellerOrReadOnly, )


class ProdutoList(ListCreateAPIView):
    """
    Lista todos os produtos existentes.\n
    Pode ser filtrada por nome, sendo ele exato, ou nomes que contenham a palavra a ser procurar\n
    Pode ser filtrada por preco_compra, sendo ele exato, maior, maior ou igual, menor ou menor ou igual\n
    Pode ser filtrada por preco_venda, sendo ele exato, maior, maior ou igual, menor ou menor ou igual\n
    Pode ser filtrada por disponivel, sendo ele true ou false\n
    Pode ser ordenada por id, nome e juros\n
    """
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer
    permission_classes = (IsSellerOrReadOnly, )

    filter_backends = (DjangoFilterBackend, OrderingFilter,)

    filterset_fields = {'nome': ['icontains', 'exact'],
                        'preco_compra': ['exact', 'lt', 'gt', 'lte', 'gte'],
                        'preco_venda': ['exact', 'lt', 'gt', 'lte', 'gte'],
                        'disponivel': ['exact', ], }

    ordering_fields = ('id', 'nome', 'juros',)


class ProdutoDetail(RetrieveUpdateDestroyAPIView):
    """
    Detalhes do produto
    """
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer
    permission_classes = (IsSellerOrReadOnly, )


class VendaList(ListCreateAPIView):
    """
    Lista todas as vendas existentes.\n
    Pode ser filtrada por pagamento\n
    Pode ser filtrada por valor_venda, sendo ele exato, maior, maior ou igual, menor ou menor ou igual\n
    Pode ser filtrada por data_venda, sendo ela exato, maior, maior ou igual, menor ou menor ou igual\n
    Pode ser ordenada por id, data_venda, valor_venda, vendedor e cliente\n
    """
    serializer_class = VendaSerializer
    permission_classes = (IsSellerOrClient, )

    filter_backends = (DjangoFilterBackend, OrderingFilter,)

    def get_queryset(self):
        user = self.request.user
        if user.is_anonymous:
            return Venda.objects.none()
        return Venda.objects.filter(Q(vendedor=user) | Q(cliente=user))

    filterset_fields = {'pagamento': ['exact'],
                        'valor_venda': ['exact', 'lt', 'gt', 'lte', 'gte'],
                        'data_venda': ['exact', 'lt', 'gt', 'lte', 'gte']}

    ordering_fields = ('id', 'data_venda', 'valor_venda', 'vendedor', 'cliente')


class VendaDetail(RetrieveUpdateDestroyAPIView):
    """
    Detalhes da venda
    """
    serializer_class = VendaSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_anonymous:
            return Venda.objects.none()
        return Venda.objects.filter(Q(vendedor=user) | Q(cliente=user))

    permission_classes = (IsSellerOrClient, )


class ProdutoMaisVendido(RetrieveAPIView):
    serializer_class = ProdutoMaisVendidoSerializer

    def get_object(self):
        try:
            return Produto.objects.get(id=ProdutoVenda.objects.values('produto').annotate(
                produtos_count=Count('produto')).order_by('-produtos_count')[0].get('produto'))
        except Produto.DoesNotExist:
            return Produto.objects.none()


class PagamentoMaisUtilizado(RetrieveAPIView):
    serializer_class = PagamentoMaisUtilizadoSerializer

    def get_object(self):
        try:
            return Pagamento.objects.get(id=Venda.objects.values('pagamento').annotate(
                pagamentos_count=Count('pagamento')).order_by('-pagamentos_count')[0].get('pagamento'))
        except Pagamento.DoesNotExist:
            return Produto.objects.none()
