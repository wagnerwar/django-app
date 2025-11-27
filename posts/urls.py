
from . import views
from django.urls import path
urlpatterns = [
    path("", views.index, name="index"),
    path("pagina/<int:pagina_id>", views.pagina, name="pagina"),
    path("post/<int:post_id>", views.post_detail, name="post_detail"),
    path("carrosseis/", views.carrossel_lista, name="carrossel_lista"),
    path("carrossel/<int:carrossel_id>/imagens/", views.carrossel_imagens, name="carrossel_imagens"),
]