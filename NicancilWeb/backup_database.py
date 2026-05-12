#!/usr/bin/env python
"""
Script de backup de base de datos
Soporta SQLite y PostgreSQL
"""
import os
import sys
from pathlib import Path
from datetime import datetime
import subprocess

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NicancilWeb.settings')
import django
django.setup()

from django.conf import settings

def backup_database():
    """Realizar backup de la base de datos"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_dir = BASE_DIR / 'backups'
    backup_dir.mkdir(exist_ok=True)
    
    db_config = settings.DATABASES['default']
    engine = db_config['ENGINE']
    
    print("=" * 60)
    print("BACKUP DE BASE DE DATOS - NicancilWeb")
    print("=" * 60)
    print()
    
    if 'sqlite' in engine:
        # Backup SQLite
        print("Detectado: SQLite")
        db_path = db_config['NAME']
        backup_file = backup_dir / f'backup_sqlite_{timestamp}.db'
        
        try:
            import shutil
            shutil.copy2(db_path, backup_file)
            print(f"✅ Backup completado: {backup_file}")
            print(f"   Tamaño: {backup_file.stat().st_size / 1024:.2f} KB")
        except Exception as e:
            print(f"❌ Error al crear backup: {e}")
            return False
            
    elif 'postgresql' in engine:
        # Backup PostgreSQL
        print("Detectado: PostgreSQL")
        
        # Obtener configuración de DATABASE_URL
        database_url = os.environ.get('DATABASE_URL')
        if not database_url:
            print("❌ DATABASE_URL no configurado")
            return False
        
        backup_file = backup_dir / f'backup_postgres_{timestamp}.dump'
        
        try:
            # Usar pg_dump
            cmd = f'pg_dump {database_url} -F c -b -v -f {backup_file}'
            subprocess.run(cmd, shell=True, check=True)
            print(f"✅ Backup completado: {backup_file}")
            print(f"   Tamaño: {backup_file.stat().st_size / 1024:.2f} KB")
        except subprocess.CalledProcessError as e:
            print(f"❌ Error al crear backup: {e}")
            return False
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    else:
        print(f"❌ Motor de base de datos no soportado: {engine}")
        return False
    
    # Limpiar backups antiguos (mantener últimos 7)
    print()
    print("Limpiando backups antiguos...")
    backups = sorted(backup_dir.glob('backup_*'), key=lambda x: x.stat().st_mtime, reverse=True)
    
    if len(backups) > 7:
        for old_backup in backups[7:]:
            old_backup.unlink()
            print(f"   Eliminado: {old_backup.name}")
    
    print()
    print(f"Total de backups: {min(len(backups), 7)}")
    print()
    print("=" * 60)
    print("BACKUP COMPLETADO EXITOSAMENTE")
    print("=" * 60)
    
    return True

if __name__ == '__main__':
    success = backup_database()
    sys.exit(0 if success else 1)
