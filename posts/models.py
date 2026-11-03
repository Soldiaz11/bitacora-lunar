from django.conf import settings
from django.db import models
from django.urls import reverse


class Post(models.Model):
    class Fase(models.TextChoices):
        NUEVA = "nueva", "Luna nueva"
        CRECIENTE = "creciente", "Creciente"
        LLENA = "llena", "Luna llena"
        MENGUANTE = "menguante", "Menguante"

    titulo = models.CharField("título", max_length=150)
    bajada = models.CharField(
        "bajada",
        max_length=220,
        blank=True,
        help_text="Una frase corta que acompañe al título.",
    )
    contenido = models.TextField("contenido")
    imagen = models.ImageField("imagen", upload_to="posts/", blank=True, null=True)
    fase = models.CharField(
        "fase lunar",
        max_length=12,
        choices=Fase.choices,
        default=Fase.LLENA,
        help_text="Bajo qué luna escribiste esto.",
    )
    autor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="posts",
        verbose_name="autor",
    )
    creado = models.DateTimeField("creado", auto_now_add=True)
    actualizado = models.DateTimeField("actualizado", auto_now=True)

    class Meta:
        ordering = ["-creado"]
        verbose_name = "publicación"
        verbose_name_plural = "publicaciones"

    def __str__(self):
        return self.titulo

    def get_absolute_url(self):
        return reverse("posts:detail", args=[self.pk])

    @property
    def minutos_lectura(self):
        return max(1, round(len(self.contenido.split()) / 200))
