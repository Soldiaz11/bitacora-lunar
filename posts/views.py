from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
)

from .forms import PostForm
from .luna import luna_de_hoy
from .models import Post


class SoloAutorMixin(UserPassesTestMixin):
    """Permite editar o eliminar un post solo a quien lo escribió."""

    def test_func(self):
        return self.get_object().autor == self.request.user

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.error(self.request, "Solo quien escribió esta entrada puede modificarla.")
            return redirect("posts:detail", pk=self.kwargs["pk"])
        return super().handle_no_permission()


class PostListView(ListView):
    model = Post
    template_name = "posts/post_list.html"
    context_object_name = "posts"
    paginate_by = 7

    def get_queryset(self):
        queryset = Post.objects.select_related("autor", "autor__perfil")
        self.query = self.request.GET.get("q", "").strip()
        self.fase = self.request.GET.get("fase", "")
        if self.query:
            queryset = queryset.filter(
                Q(titulo__icontains=self.query)
                | Q(bajada__icontains=self.query)
                | Q(contenido__icontains=self.query)
            )
        if self.fase in Post.Fase.values:
            queryset = queryset.filter(fase=self.fase)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        parametros = self.request.GET.copy()
        parametros.pop("page", None)
        context.update(
            query=self.query,
            fase_activa=self.fase,
            fases=Post.Fase.choices,
            parametros=parametros.urlencode(),
            filtrando=bool(self.query or self.fase in Post.Fase.values),
            luna=luna_de_hoy(),
        )
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = "posts/post_detail.html"
    queryset = Post.objects.select_related("autor", "autor__perfil")


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "posts/post_form.html"

    def get_initial(self):
        return {"fase": luna_de_hoy()["simple"]}

    def form_valid(self, form):
        form.instance.autor = self.request.user
        messages.success(self.request, "Entrada publicada.")
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, SoloAutorMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "posts/post_form.html"

    def form_valid(self, form):
        messages.success(self.request, "Cambios guardados.")
        return super().form_valid(form)


class PostDeleteView(LoginRequiredMixin, SoloAutorMixin, DeleteView):
    model = Post
    template_name = "posts/post_confirm_delete.html"
    success_url = reverse_lazy("posts:list")

    def form_valid(self, form):
        messages.success(self.request, "Entrada eliminada.")
        return super().form_valid(form)


class AcercaView(TemplateView):
    template_name = "posts/acerca.html"
