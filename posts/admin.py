from django.contrib import admin

from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("titulo", "autor", "fase", "creado")
    list_filter = ("fase", "creado")
    search_fields = ("titulo", "contenido")
