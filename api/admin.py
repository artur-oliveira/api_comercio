from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.forms import ModelForm
from .models import (User,
                     Categoria,
                     Pagamento,
                     Produto,
                     ProdutoVenda,
                     Venda)


class UserCreationForm(ModelForm):
    class Meta:
        model = User
        fields = ('is_client', 'is_seller')

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class CustomUserAdmin(UserAdmin):
    # The forms to add and change user instances
    add_form = UserCreationForm
    list_display = ("username",)
    ordering = ("username",)

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password', 'first_name', 'last_name')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password', 'first_name', 'last_name', 'is_superuser', 'is_staff',
                       'is_active', 'is_seller', 'is_client')}
         ),
    )

    filter_horizontal = ()


admin.site.register(User, CustomUserAdmin)
admin.site.register(Categoria)
admin.site.register(Pagamento)
admin.site.register(Produto)
admin.site.register(ProdutoVenda)
admin.site.register(Venda)
