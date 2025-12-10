from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Perfil

class RegistroForm(UserCreationForm):
    tipo = forms.ChoiceField(choices=Perfil.TIPO_CHOICES, label='Tipo de Usuário')
    telefone = forms.CharField(max_length=15, required=False, label='Telefone')
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'tipo', 'telefone']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            perfil = Perfil.objects.create(
                usuario=user,
                tipo=self.cleaned_data['tipo'],
                telefone=self.cleaned_data['telefone']
            )
        return user