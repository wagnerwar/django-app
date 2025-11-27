from django.contrib import admin

# Register your models here.
from .models import Post, Categoria, Tag, Pagina, Imagem, Logo, Carrossel, ImagemCarrossel

admin.site.register(Post)
admin.site.register(Categoria)
admin.site.register(Tag)
admin.site.register(Pagina)
admin.site.register(Imagem)
admin.site.register(Carrossel)
admin.site.register(ImagemCarrossel)

@admin.register(Logo)
class LogoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'atualizado_em')
    
    def has_add_permission(self, request):
        # Permite adicionar apenas se não existe nenhum logo
        return not Logo.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Não permite deletar o logo
        return False
