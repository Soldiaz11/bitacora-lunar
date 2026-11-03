from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from posts.models import Post

ENTRADAS = [
    (
        "La ciudad apaga sus luces de a una",
        "Un inventario de ventanas encendidas a las tres de la mañana.",
        "llena",
        "Desde el balcón se ve un edificio entero. A medianoche quedaban once ventanas "
        "encendidas; a la una, siete; a las tres, solamente dos.\n\n"
        "En una alguien cocina. En la otra hay una lámpara verde que no se apaga nunca, "
        "y me gusta imaginar que quien vive ahí también está mirando para afuera, "
        "contando las mías.\n\n"
        "La luna llena hace que todo parezca un escenario a punto de empezar.",
    ),
    (
        "Instrucciones para mirar el cielo sin telescopio",
        "No hace falta equipo. Hace falta paciencia y apagar el celular.",
        "nueva",
        "Primero, buscá el lugar más oscuro que tengas cerca. Una terraza sirve.\n\n"
        "Segundo, esperá veinte minutos. Los ojos tardan en acostumbrarse a la oscuridad "
        "y cada vez que mirás una pantalla volvés a empezar.\n\n"
        "Tercero, no busques nada en particular. Las estrellas aparecen solas, de a poco, "
        "como gente que llega tarde a una fiesta.",
    ),
    (
        "Mate a las cuatro de la mañana",
        "Hay conversaciones que solamente existen a esta hora.",
        "creciente",
        "El agua tiene que estar a punto, no hervida. Eso me lo enseñó mi abuelo, que "
        "también se despertaba temprano sin motivo.\n\n"
        "A esta hora la casa hace ruidos que de día no se escuchan: la heladera, un caño, "
        "el perro del vecino que sueña en voz alta.",
    ),
    (
        "Todo lo que se pierde en una mudanza",
        "Una caja que dice «varios» y nunca se vuelve a abrir.",
        "menguante",
        "Las mudanzas te obligan a decidir qué vale la pena cargar. Libros, sí. "
        "Cables viejos, misteriosamente también.\n\n"
        "Lo que nunca entra en ninguna caja es la luz de la ventana de la cocina a las "
        "siete de la tarde. Esa se queda.",
    ),
    (
        "El colectivo de la madrugada",
        "Cuarenta minutos, seis pasajeros, ningún apuro.",
        "creciente",
        "El chofer escucha una radio de tangos bajita. Nadie habla.\n\n"
        "Hay algo de tregua en los viajes de madrugada: todos vamos a algún lado, "
        "pero nadie está corriendo todavía.",
    ),
    (
        "Cuaderno de sueños, semana uno",
        "Intenté anotar todo lo que soñaba durante siete días.",
        "nueva",
        "Lunes: una biblioteca inundada donde los libros flotaban abiertos.\n\n"
        "Martes: nada. O nada que haya sobrevivido al despertador.\n\n"
        "Miércoles: volvía a la escuela primaria, pero el patio era un muelle.",
    ),
]


class Command(BaseCommand):
    help = "Crea una autora de ejemplo y algunas entradas para probar el blog."

    def handle(self, *args, **options):
        autora, creada = User.objects.get_or_create(
            username="selene", defaults={"first_name": "Selene", "email": "selene@example.com"}
        )
        if creada:
            autora.set_unusable_password()
            autora.save()
            autora.perfil.ciudad = "Buenos Aires"
            autora.perfil.bio = "Escribo cuando el resto duerme."
            autora.perfil.save()

        nuevas = 0
        for titulo, bajada, fase, contenido in ENTRADAS:
            _, creado = Post.objects.get_or_create(
                titulo=titulo,
                defaults={"bajada": bajada, "fase": fase, "contenido": contenido, "autor": autora},
            )
            nuevas += creado
        self.stdout.write(self.style.SUCCESS(f"Listo: {nuevas} entradas de ejemplo creadas."))
