import shutil
import tempfile
from io import BytesIO

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from PIL import Image

from .luna import camino_svg, fase_simple
from .models import Post

MEDIA_TEMPORAL = tempfile.mkdtemp()


def imagen_de_prueba():
    buffer = BytesIO()
    Image.new("RGB", (20, 20), "navy").save(buffer, format="PNG")
    return SimpleUploadedFile("prueba.png", buffer.getvalue(), content_type="image/png")


@override_settings(MEDIA_ROOT=MEDIA_TEMPORAL)
class PostTests(TestCase):
    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(MEDIA_TEMPORAL, ignore_errors=True)
        super().tearDownClass()

    def setUp(self):
        self.autora = User.objects.create_user("ana", password="clave-de-prueba-123")
        self.otro = User.objects.create_user("beto", password="clave-de-prueba-123")
        self.post = Post.objects.create(
            titulo="Noche de prueba", contenido="Texto sobre estrellas", autor=self.autora
        )

    def test_listado_y_detalle_para_anonimos(self):
        self.assertContains(self.client.get(reverse("posts:list")), "Noche de prueba")
        respuesta = self.client.get(self.post.get_absolute_url())
        self.assertContains(respuesta, "portada-vacia")  # sin imagen el template no se rompe

    def test_rutas_protegidas_redirigen_al_login(self):
        for nombre, args in [
            ("posts:create", []),
            ("posts:update", [self.post.pk]),
            ("posts:delete", [self.post.pk]),
            ("accounts:editar_perfil", []),
        ]:
            respuesta = self.client.get(reverse(nombre, args=args))
            self.assertRedirects(respuesta, f"{reverse('accounts:login')}?next={reverse(nombre, args=args)}")

    def test_crear_post_con_imagen(self):
        self.client.login(username="ana", password="clave-de-prueba-123")
        respuesta = self.client.post(
            reverse("posts:create"),
            {"titulo": "Con foto", "contenido": "Hola", "fase": "llena", "imagen": imagen_de_prueba()},
        )
        nuevo = Post.objects.get(titulo="Con foto")
        self.assertRedirects(respuesta, nuevo.get_absolute_url())
        self.assertEqual(nuevo.autor, self.autora)
        self.assertContains(self.client.get(nuevo.get_absolute_url()), nuevo.imagen.url)

    def test_editar_y_eliminar_propio(self):
        self.client.login(username="ana", password="clave-de-prueba-123")
        self.client.post(
            reverse("posts:update", args=[self.post.pk]),
            {"titulo": "Editado", "contenido": "Nuevo", "fase": "nueva"},
        )
        self.post.refresh_from_db()
        self.assertEqual(self.post.titulo, "Editado")
        self.client.post(reverse("posts:delete", args=[self.post.pk]))
        self.assertFalse(Post.objects.exists())

    def test_otro_usuario_no_puede_editar(self):
        self.client.login(username="beto", password="clave-de-prueba-123")
        respuesta = self.client.post(
            reverse("posts:update", args=[self.post.pk]),
            {"titulo": "Hackeado", "contenido": "x", "fase": "nueva"},
        )
        self.assertRedirects(respuesta, self.post.get_absolute_url())
        self.post.refresh_from_db()
        self.assertEqual(self.post.titulo, "Noche de prueba")

    def test_busqueda(self):
        url = reverse("posts:list")
        self.assertContains(self.client.get(url, {"q": "estrellas"}), "Noche de prueba")
        self.assertContains(self.client.get(url, {"q": "xyz123"}), "No hay entradas que coincidan")

    def test_luna(self):
        self.assertEqual(fase_simple(0.5), "llena")
        self.assertTrue(camino_svg(0.25).startswith("M100 10"))


class CuentaTests(TestCase):
    def test_registro_login_logout(self):
        respuesta = self.client.post(
            reverse("accounts:registro"),
            {"username": "nueva", "email": "nueva@example.com",
             "password1": "unaClaveLarga987", "password2": "unaClaveLarga987"},
        )
        self.assertRedirects(respuesta, reverse("posts:list"))
        usuario = User.objects.get(username="nueva")
        self.assertTrue(hasattr(usuario, "perfil"))
        self.assertContains(self.client.get(reverse("posts:list")), "Salir")

        self.client.post(reverse("accounts:logout"))
        self.assertContains(self.client.get(reverse("posts:list")), "Crear cuenta")

        self.assertTrue(self.client.login(username="nueva", password="unaClaveLarga987"))

    def test_perfil_publico(self):
        User.objects.create_user("lu", password="clave-de-prueba-123")
        self.assertContains(self.client.get(reverse("accounts:perfil", args=["lu"])), "lu")
