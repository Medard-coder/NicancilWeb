from django.core.management.base import BaseCommand
from django.utils import timezone
from rentas.models import Renta

class Command(BaseCommand):
    help = 'Actualiza automáticamente las rentas vencidas a estado pendiente de devolución'

    def handle(self, *args, **options):
        rentas_vencidas = Renta.objects.filter(
            estado='activa',
            fecha_fin__lt=timezone.now()
        )
        
        count = rentas_vencidas.count()
        rentas_vencidas.update(estado='pendiente_devolucion')
        
        self.stdout.write(
            self.style.SUCCESS(f'Se actualizaron {count} rentas vencidas a estado pendiente de devolución')
        )