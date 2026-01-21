from django import forms
from .models import Solicitacao


class SolicitacaoForm(forms.ModelForm):
    class Meta:
        model = Solicitacao
        fields = ['nome', 'cpf', 'descricao']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite seu nome completo',
                'required': True
            }),
            'cpf': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '000.000.000-00',
                'required': True,
                'maxlength': '14'
            }),
            'descricao': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Descreva sua solicitação...',
                'rows': 5,
                'required': True
            }),
        }
        labels = {
            'nome': 'Nome Completo',
            'cpf': 'CPF',
            'descricao': 'Descrição da Solicitação'
        }
        help_texts = {
            'cpf': 'Digite seu CPF com pontos e traço (000.000.000-00)'
        }
