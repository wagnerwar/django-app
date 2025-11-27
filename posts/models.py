from django.db import models
from django.core.files.base import ContentFile
from PIL import Image
from io import BytesIO

from ckeditor.fields import RichTextField

# Create your models here.

class Categoria(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    conteudo = models.CharField(max_length=200)
    def __str__(self):
        return self.nome
    

class Tag(models.Model):
    nome = models.CharField(max_length=50, unique=True)
    def __str__(self):
        return self.nome


class Post(models.Model):
    conteudo = RichTextField(config_name='awesome_ckeditor')
    pub_date = models.DateTimeField("date published")
    titulo = models.CharField(max_length=100)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='posts', null=True)
    tags = models.ManyToManyField(Tag, related_name='posts', blank=True)
    def __str__(self):
        return self.titulo

class Pagina(models.Model):
    titulo = models.CharField(max_length=100, unique=True)
    conteudo = RichTextField(config_name='awesome_ckeditor')
    ativo = models.BooleanField(default=True)
    def __str__(self):
        return self.titulo
    
# Modelo para upload de imagem
class Imagem(models.Model):
    titulo = models.CharField(max_length=100)
    imagem = models.ImageField(upload_to='imagens/')
    criado_em = models.DateTimeField(auto_now_add=True)
    ativo = models.BooleanField(default=True)
    def __str__(self):
        return self.titulo

# Modelo para o logo do site (apenas um registro permitido)
class Logo(models.Model):
    titulo = models.CharField(max_length=100, default="Logo do Site")
    imagem = models.ImageField(upload_to='logo/')
    atualizado_em = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Logo do Site"
        verbose_name_plural = "Logo do Site"
    
    def save(self, *args, **kwargs):
        # Garante que só existe um registro
        if not self.pk and Logo.objects.exists():
            # Se já existe um logo, atualiza ele ao invés de criar novo
            logo_existente = Logo.objects.first()
            self.pk = logo_existente.pk
        super(Logo, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.titulo


# Modelo para Carrossel de Imagens
class Carrossel(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    ativo = models.BooleanField(default=True, verbose_name="Status")
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Carrossel"
        verbose_name_plural = "Carrosséis"
    
    def __str__(self):
        return self.nome


# Modelo para Imagens do Carrossel
class ImagemCarrossel(models.Model):
    carrossel = models.ForeignKey(Carrossel, on_delete=models.CASCADE, related_name='imagens')
    titulo = models.CharField(max_length=100)
    imagem = models.ImageField(upload_to='carrossel/')
    ordem = models.PositiveIntegerField(default=0, help_text="Ordem de exibição da imagem")
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Imagem do Carrossel"
        verbose_name_plural = "Imagens do Carrossel"
        ordering = ['ordem', 'criado_em']
    
    def save(self, *args, **kwargs):
        # Redimensiona a imagem para 250x250 antes de salvar
        if self.imagem:
            img = Image.open(self.imagem)
            
            # Converte para RGB se necessário (para suportar PNG com transparência)
            if img.mode in ('RGBA', 'LA', 'P'):
                # Cria um fundo branco
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = background
            elif img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Redimensiona para 250x250
            img = img.resize((250, 250), Image.LANCZOS)
            
            # Salva a imagem redimensionada em um buffer
            buffer = BytesIO()
            img.save(buffer, format='JPEG', quality=85)
            buffer.seek(0)
            
            # Substitui o arquivo original pelo redimensionado
            self.imagem.save(
                self.imagem.name,
                ContentFile(buffer.read()),
                save=False
            )
        
        super(ImagemCarrossel, self).save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.carrossel.nome} - {self.titulo}"
