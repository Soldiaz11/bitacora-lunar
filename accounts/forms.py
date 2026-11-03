from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Perfil


class RegistroForm(UserCreationForm):
    email = forms.EmailField(label="Email", required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ["username", "email"]


class UsuarioForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]


class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ["avatar", "ciudad", "bio"]
        widgets = {"bio": forms.Textarea(attrs={"rows": 4})}
