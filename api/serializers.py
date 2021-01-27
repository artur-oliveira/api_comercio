from rest_framework import serializers
from .models import (Categoria,
                     User,
                     Pagamento,
                     Produto,
                     ProdutoVenda,
                     Venda,
                     )


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'is_client', 'is_seller')


class CategoriaSerializer(serializers.HyperlinkedModelSerializer):
    def __init__(self, *args, **kwargs):
        super(CategoriaSerializer, self).__init__(*args, **kwargs)
        if 'context' in kwargs:
            if 'request' in kwargs['context']:
                request = kwargs.get('context').get('request')
                user = request.user
                existing = set(self.fields.keys())

                if user.is_anonymous or user.is_client:
                    for other in existing - {'url', 'nome', }:
                        self.fields.pop(other)

    class Meta:
        model = Categoria
        fields = ('id', 'url', 'nome', )


class PagamentoSerializer(serializers.HyperlinkedModelSerializer):
    def __init__(self, *args, **kwargs):
        super(PagamentoSerializer, self).__init__(*args, **kwargs)
        if 'context' in kwargs:
            if 'request' in kwargs['context']:
                request = kwargs.get('context').get('request')
                user = request.user
                existing = set(self.fields.keys())

                if user.is_anonymous or user.is_client:
                    for other in existing - {'url', 'nome', }:
                        self.fields.pop(other)

    class Meta:
        model = Pagamento
        fields = ('id', 'url', 'nome', 'juros')


class ProdutoSerializer(serializers.HyperlinkedModelSerializer):
    def __init__(self, *args, **kwargs):
        super(ProdutoSerializer, self).__init__(*args, **kwargs)
        if 'context' in kwargs:
            if 'request' in kwargs['context']:
                request = kwargs.get('context').get('request')
                user = request.user

                existing = set(self.fields.keys())

                if user.is_anonymous or user.is_client:
                    allow = {'url', 'nome', 'preco_venda', 'disponivel', 'categoria', }

                    for other in existing - allow:
                        self.fields.pop(other)

    class Meta:
        model = Produto
        fields = ('id', 'url', 'nome', 'preco_compra', 'preco_venda', 'quantidade', 'disponivel', 'categoria', )
        read_only_fields = ('disponivel', )


class ProdutoVendaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProdutoVenda
        fields = ('produto', 'quantidade')

    @classmethod
    def validate_produto(cls, produto):
        if not produto.disponivel:
            raise serializers.ValidationError("Este produto não está disponível")
        return produto


"""
{
    "pagamento": "http://localhost:8000/api/v1/pagamento/1",
    "produtos": [
{"produto": "http://localhost:8000/api/v1/produto/1", "quantidade": 2
}
],
    "cliente": "http://localhost:8000/api/v1/users/3",
    "vendedor": "http://localhost:8000/api/v1/users/2"
}"""


class VendaSerializer(serializers.HyperlinkedModelSerializer):
    produtos = ProdutoVendaSerializer(source='produtovenda_set', many=True)

    class Meta:
        model = Venda
        fields = ('id', 'url', 'pagamento', 'produtos', 'valor_venda', 'cliente', 'vendedor', 'data_venda', )
        read_only_fields = ('valor_venda', )

    @classmethod
    def validate_produtos(cls, produtos):
        for data in produtos:
            quantidade = data.get('quantidade')
            produto = data.get('produto')
            if quantidade > produto.quantidade:
                raise serializers.ValidationError(
                    'O produto %s possui apenas %d em estoque' % (produto.nome, produto.quantidade))

        return produtos

    def validate_vendedor(self, vendedor) -> User:
        if self.context.get('request').user == vendedor:
            return vendedor

        raise serializers.ValidationError('Você não pode realizar uma venda usando outro vendedor')

    def create(self, validated_data) -> Venda:
        valor = 0
        instance: Venda = Venda(pagamento=validated_data.pop('pagamento'),
                                cliente=validated_data.pop('cliente'),
                                vendedor=validated_data.pop('vendedor'), )

        instance.save()

        for data in validated_data.pop('produtovenda_set'):
            produto: Produto = data.get('produto')
            quantidade = data.get('quantidade')

            valor += produto.preco_venda * quantidade
            ProdutoVenda(venda=instance, produto=produto, quantidade=quantidade).save()

            produto.quantidade -= quantidade
            produto.save()

        instance.valor_venda = valor + (valor * (instance.pagamento.juros / 100))
        instance.save()

        return instance
