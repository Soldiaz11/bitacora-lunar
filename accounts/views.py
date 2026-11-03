from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import CreateView

from .forms import PerfilForm, RegistroForm, UsuarioForm
from .models import Perfil


class RegistroView(CreateView):
    form_class = RegistroForm
    template_name = "accounts/registro.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("posts:list")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        usuario = form.save()
        login(self.request, usuario)
        messages.success(self.request, f"Bienvenida/o, {usuario.username}. Ya podés escribir tu primera entrada.")
        return redirect("posts:list")


def perfil(request, username):
    autor = get_object_or_404(User, username=username)
    Perfil.objects.get_or_create(usuario=autor)
    return render(
        request,
        "accounts/perfil.html",
        {"autor": autor, "posts": autor.posts.all(), "es_propio": request.user == autor},
    )


@login_required
def mi_perfil(request):
    return redirect("accounts:perfil", username=request.user.username)


@login_required
def editar_perfil(request):
    perfil_usuario, _ = Perfil.objects.get_or_create(usuario=request.user)
    if request.method == "POST":
        usuario_form = UsuarioForm(request.POST, instance=request.user)
        perfil_form = PerfilForm(request.POST, request.FILES, instance=perfil_usuario)
        if usuario_form.is_valid() and perfil_form.is_valid():
            usuario_form.save()
            perfil_form.save()
            messages.success(request, "Perfil actualizado.")
            return redirect("accounts:mi_perfil")
    else:
        usuario_form = UsuarioForm(instance=request.user)
        perfil_form = PerfilForm(instance=perfil_usuario)
    return render(
        request,
        "accounts/editar_perfil.html",
        {"usuario_form": usuario_form, "perfil_form": perfil_form},
    )
