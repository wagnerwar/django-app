from posts.models import Pagina, Logo

def global_context(request):
    logo = Logo.objects.first()
    return {
        'nome_site': 'Meu Site',
        'ano_atual': 2025,
        'menu_paginas': Pagina.objects.filter(ativo=True),
        'logo': logo,
    }