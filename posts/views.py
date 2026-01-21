from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.template import loader
from .models import Post, Pagina, Carrossel, ImagemCarrossel, Solicitacao
from .forms import SolicitacaoForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.contrib import messages

# Create your views here.
def index(request):
    post_list = Post.objects.order_by("-pub_date")
    
    # Captura o termo de pesquisa
    query = request.GET.get('q')
    if query:
        # Pesquisa no título e no conteúdo dos posts
        post_list = post_list.filter(
            Q(titulo__icontains=query) | Q(conteudo__icontains=query)
        )
    
    paginator = Paginator(post_list, 5)  # 5 postagens por página
    page = request.GET.get('page')
    try:
        lista = paginator.page(page)
    except PageNotAnInteger:
        lista = paginator.page(1)
    except EmptyPage:
        lista = paginator.page(paginator.num_pages)
    context = {"lista": lista, "query": query}
    return render(request, "posts/index.html", context)

def pagina(request, pagina_id):
    pagina_obj = get_object_or_404(Pagina, pk=pagina_id)
    context = {"pagina": pagina_obj}
    return render(request, "posts/pagina.html", context)

def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    context = {"post": post}
    return render(request, "posts/post_detail.html", context)

def carrossel_lista(request):
    """Lista todos os carrosséis ativos"""
    carrosseis = Carrossel.objects.filter(ativo=True).order_by('-atualizado_em')
    context = {"carrosseis": carrosseis}
    return render(request, "posts/carrossel_lista.html", context)

def carrossel_imagens(request, carrossel_id):
    """Exibe as imagens de um carrossel específico"""
    carrossel = get_object_or_404(Carrossel, pk=carrossel_id, ativo=True)
    imagens = carrossel.imagens.filter(ativo=True).order_by('ordem', 'criado_em')
    context = {
        "carrossel": carrossel,
        "imagens": imagens
    }
    return render(request, "posts/carrossel_imagens.html", context)


def solicitacao_form(request):
    """Formulário para cadastrar uma nova solicitação"""
    if request.method == 'POST':
        form = SolicitacaoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Solicitação enviada com sucesso!')
            return redirect('solicitacao_form')
        else:
            messages.error(request, 'Por favor, corrija os erros no formulário.')
    else:
        form = SolicitacaoForm()
    
    context = {'form': form}
    return render(request, 'posts/solicitacao_form.html', context)

