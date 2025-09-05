from django.db import migrations

def migrate_cliente_data(apps, schema_editor):
    # Obtener los modelos
    InventarioCliente = apps.get_model('inventario', 'Cliente')
    RentasCliente = apps.get_model('rentas', 'Cliente')
    Renta = apps.get_model('rentas', 'Renta')
    
    # Crear un mapeo de IDs antiguos a nuevos
    id_mapping = {}
    
    # Copiar todos los clientes de inventario a rentas
    for cliente in InventarioCliente.objects.all():
        nuevo_cliente = RentasCliente.objects.create(
            nombre=cliente.nombre,
            telefono=cliente.telefono,
            correo=cliente.correo,
            direccion=cliente.direccion,
            fecha_registro=cliente.fecha_registro
        )
        id_mapping[cliente.id] = nuevo_cliente.id
    
    # Actualizar las referencias en las rentas
    for renta in Renta.objects.all():
        if renta.cliente_id in id_mapping:
            renta.cliente_id = id_mapping[renta.cliente_id]
            renta.save()

def reverse_migrate_cliente_data(apps, schema_editor):
    # Para revertir, eliminar todos los clientes de rentas
    RentasCliente = apps.get_model('rentas', 'Cliente')
    RentasCliente.objects.all().delete()

class Migration(migrations.Migration):
    dependencies = [
        ('rentas', '0002_cliente_alter_renta_cliente'),
        ('inventario', '0005_cliente'),
    ]

    operations = [
        migrations.RunPython(migrate_cliente_data, reverse_migrate_cliente_data),
    ]