from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path("registro/", views.RegistroView.as_view(), name="registro"),
    path(
        "entrar/",
        auth_views.LoginView.as_view(
            template_name="accounts/login.html", redirect_authenticated_user=True
        ),
        name="login",
    ),
    path("salir/", auth_views.LogoutView.as_view(), name="logout"),
    path("perfil/", views.mi_perfil, name="mi_perfil"),
    path("perfil/editar/", views.editar_perfil, name="editar_perfil"),
    path("autores/<str:username>/", views.perfil, name="perfil"),
]
