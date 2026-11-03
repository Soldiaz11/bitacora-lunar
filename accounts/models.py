from django.conf import settings
from django.db import models


class Perfil(models.Model):
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="perfil"
    )
    avatar = models.ImageField("foto de perfil", upload_to="avatares/", blank=True, null=True)
    bio = models.TextField("sobre mí", max_length=300, blank=True)
    ciudad = models.CharField("ciudad", max_length=80, blank=True)

    class Meta:
        verbose_name = "perfil"
        verbose_name_plural = "perfiles"

    def __str__(self):
        return f"Perfil de {self.usuario.username}"
