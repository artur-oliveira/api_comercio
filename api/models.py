from decimal import Decimal

from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models


class User(AbstractUser):
    is_client = models.BooleanField(default=False,
                                    verbose_name="Cliente",
                                    help_text="Se o usuário for do tipo cliente, ele irá ver apenas informações "
                                              "relacionadas a ele, além de não poder alterar os dados do sistema")
    is_seller = models.BooleanField(default=False,
                                    verbose_name="Vendedor",
                                    help_text="Se o usuário for do tipo vendedor, ele poderá adicionar, deletar ou "
                                              "excluir, além de poder ver consumir urls específicas")


class Categoria(models.Model):
    nome = models.CharField(max_length=255, unique=True)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.nome = self.nome.upper()
        super(Categoria, self).save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return self.nome

    def __repr__(self):
        return self.__str__()


class Pagamento(models.Model):
    nome = models.CharField(max_length=255, unique=True)
    juros = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0'))])

    def __str__(self):
        return self.nome

    def __repr__(self):
        return self.__str__()


class Produto(models.Model):
    nome = models.CharField(max_length=255)
    preco_compra = models.DecimalField(max_digits=20, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    preco_venda = models.DecimalField(max_digits=20, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    quantidade = models.IntegerField(validators=[MinValueValidator(0)])
    disponivel = models.BooleanField()
    categoria = models.ForeignKey('Categoria', on_delete=models.CASCADE)
    
    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.nome = self.nome.upper()
        self.disponivel = self.quantidade > 0
        super(Produto, self).save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return self.nome

    def __repr__(self):
        return self.__str__()


class ProdutoVenda(models.Model):
    venda = models.ForeignKey('Venda', on_delete=models.CASCADE)
    produto = models.ForeignKey('Produto', on_delete=models.CASCADE)
    quantidade = models.IntegerField(validators=[MinValueValidator(1)])

    def __str__(self):
        return '%s %s %s' % (self.venda, self.produto, self.quantidade)


class Venda(models.Model):
    pagamento = models.ForeignKey('Pagamento', on_delete=models.CASCADE)
    produtos = models.ManyToManyField('Produto', through='ProdutoVenda')
    data_venda = models.DateField(auto_now_add=True)
    vendedor = models.ForeignKey('User', related_name='vendedor', on_delete=models.CASCADE)
    cliente = models.ForeignKey('User', related_name='cliente', on_delete=models.CASCADE)
    valor_venda = models.DecimalField(max_digits=50, decimal_places=2, default=0)

    def __str__(self):
        return self.vendedor.username

    def __repr__(self):
        return self.__str__()
