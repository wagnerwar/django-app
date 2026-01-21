from django.contrib import admin

# Register your models here.
from .models import Post, Categoria, Tag, Pagina, Imagem, Logo, Carrossel, ImagemCarrossel, Solicitacao

admin.site.register(Post)
admin.site.register(Categoria)
admin.site.register(Tag)
admin.site.register(Pagina)
admin.site.register(Imagem)


# Inline para gerenciar as imagens dentro do carrossel
class ImagemCarrosselInline(admin.TabularInline):
    model = ImagemCarrossel
    extra = 1  # Número de formulários vazios extras para adicionar novas imagens
    fields = ('titulo', 'imagem', 'ordem', 'ativo')
    ordering = ['ordem']


@admin.register(Carrossel)
class CarrosselAdmin(admin.ModelAdmin):
    list_display = ('nome', 'ativo', 'criado_em', 'atualizado_em')
    list_filter = ('ativo',)
    search_fields = ('nome',)
    inlines = [ImagemCarrosselInline]


@admin.register(Logo)
class LogoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'atualizado_em')
    
    def has_add_permission(self, request):
        # Permite adicionar apenas se não existe nenhum logo
        return not Logo.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Não permite deletar o logo
        return False


@admin.register(Solicitacao)
class SolicitacaoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cpf', 'data', 'descricao_resumida')
    list_filter = ('data',)
    search_fields = ('nome', 'cpf', 'descricao')
    readonly_fields = ('data',)
    date_hierarchy = 'data'
    ordering = ('-data',)
    
    def descricao_resumida(self, obj):
        """Mostra apenas os primeiros 50 caracteres da descrição"""
        if len(obj.descricao) > 50:
            return f"{obj.descricao[:50]}..."
        return obj.descricao
    descricao_resumida.short_description = 'Descrição'
    
    # Remove o botão de adicionar no admin (já que a inclusão é via portal)
    def has_add_permission(self, request):
        return False
