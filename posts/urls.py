from django.urls import path

from . import views

app_name = "posts"

urlpatterns = [
    path("", views.PostListView.as_view(), name="list"),
    path("acerca/", views.AcercaView.as_view(), name="acerca"),
    path("entradas/nueva/", views.PostCreateView.as_view(), name="create"),
    path("entradas/<int:pk>/", views.PostDetailView.as_view(), name="detail"),
    path("entradas/<int:pk>/editar/", views.PostUpdateView.as_view(), name="update"),
    path("entradas/<int:pk>/eliminar/", views.PostDeleteView.as_view(), name="delete"),
]
