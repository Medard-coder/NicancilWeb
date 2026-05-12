# Guía de Configuración de PostgreSQL - NicancilWeb

## 📋 Configuración Implementada

El proyecto ahora soporta **dos modos de base de datos**:

- **Desarrollo**: SQLite (automático, sin configuración)
- **Producción**: PostgreSQL (configurado via DATABASE_URL)

---

## 🔧 Configuración para Desarrollo (SQLite)

**No requiere configuración adicional**. Si no existe `DATABASE_URL` en el archivo `.env`, automáticamente usará SQLite.

```bash
# En .env - dejar DATABASE_URL sin configurar o comentado
# DATABASE_URL=  (vacío o comentado)
```

El proyecto funcionará con `db.sqlite3` como siempre.

---

## 🚀 Configuración para Producción (PostgreSQL)

### **Paso 1: Instalar PostgreSQL**

#### En Ubuntu/Debian:
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
```

#### En Windows:
- Descargar desde: https://www.postgresql.org/download/windows/
- Instalar PostgreSQL 15 o superior

#### En macOS:
```bash
brew install postgresql@15
brew services start postgresql@15
```

---

### **Paso 2: Crear Base de Datos y Usuario**

```bash
# Acceder a PostgreSQL
sudo -u postgres psql

# Crear base de datos
CREATE DATABASE nicancilweb_db;

# Crear usuario
CREATE USER nicancil_user WITH PASSWORD 'tu_password_super_seguro';

# Otorgar privilegios
ALTER ROLE nicancil_user SET client_encoding TO 'utf8';
ALTER ROLE nicancil_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE nicancil_user SET timezone TO 'America/Mexico_City';
GRANT ALL PRIVILEGES ON DATABASE nicancilweb_db TO nicancil_user;

# Salir
\q
```

---

### **Paso 3: Configurar Variables de Entorno**

Edita tu archivo `.env` y agrega:

```bash
# Configuración de PostgreSQL
DATABASE_URL=postgresql://nicancil_user:tu_password_super_seguro@localhost:5432/nicancilweb_db
```

**Formato de DATABASE_URL:**
```
postgresql://[usuario]:[password]@[host]:[puerto]/[nombre_db]
```

**Ejemplos:**

```bash
# Local
DATABASE_URL=postgresql://nicancil_user:mipassword@localhost:5432/nicancilweb_db

# Servidor remoto
DATABASE_URL=postgresql://nicancil_user:mipassword@192.168.1.100:5432/nicancilweb_db

# Heroku (automático)
DATABASE_URL=postgres://usuario:pass@host.compute.amazonaws.com:5432/dbname

# Railway (automático)
DATABASE_URL=postgresql://postgres:pass@containers.railway.app:1234/railway

# Render (automático)
DATABASE_URL=postgresql://user:pass@dpg-xxxxx.oregon-postgres.render.com/dbname
```

---

### **Paso 4: Instalar Dependencias**

```bash
# Instalar psycopg2 (driver de PostgreSQL)
pip install -r requirements.txt
```

---

### **Paso 5: Migrar Base de Datos**

```bash
# Ejecutar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Verificar conexión
python manage.py dbshell
```

---

## 🔄 Migración de SQLite a PostgreSQL

Si ya tienes datos en SQLite y quieres migrarlos a PostgreSQL:

### **Opción 1: Usando dumpdata/loaddata**

```bash
# 1. Exportar datos de SQLite
python manage.py dumpdata --natural-foreign --natural-primary \
  --exclude auth.permission --exclude contenttypes \
  --indent 2 > datadump.json

# 2. Configurar DATABASE_URL para PostgreSQL en .env
DATABASE_URL=postgresql://nicancil_user:password@localhost:5432/nicancilweb_db

# 3. Ejecutar migraciones en PostgreSQL
python manage.py migrate

# 4. Importar datos
python manage.py loaddata datadump.json

# 5. Crear superusuario si es necesario
python manage.py createsuperuser
```

### **Opción 2: Usando pgloader (Recomendado para grandes volúmenes)**

```bash
# Instalar pgloader
sudo apt install pgloader  # Ubuntu/Debian

# Crear archivo de configuración
cat > migrate.load << EOF
LOAD DATABASE
  FROM sqlite://db.sqlite3
  INTO postgresql://nicancil_user:password@localhost/nicancilweb_db
  WITH include drop, create tables, create indexes, reset sequences
  SET work_mem to '16MB', maintenance_work_mem to '512 MB';
EOF

# Ejecutar migración
pgloader migrate.load
```

---

## 🧪 Verificación

### **Verificar que estás usando PostgreSQL:**

```python
# En Django shell
python manage.py shell

>>> from django.db import connection
>>> print(connection.settings_dict['ENGINE'])
# Debe mostrar: django.db.backends.postgresql
```

### **Verificar conexión:**

```bash
# Acceder a la base de datos directamente
python manage.py dbshell

# Listar tablas
\dt

# Salir
\q
```

---

## 📊 Optimizaciones para PostgreSQL

### **1. Índices Recomendados**

Crea un archivo `add_indexes.sql`:

```sql
-- Índices para mejorar performance
CREATE INDEX idx_renta_cliente ON rentas_renta(cliente_id);
CREATE INDEX idx_renta_estado ON rentas_renta(estado);
CREATE INDEX idx_renta_fecha_fin ON rentas_renta(fecha_fin);
CREATE INDEX idx_prenda_tipo ON inventario_prenda(tipo);
CREATE INDEX idx_prenda_estatus ON inventario_prenda(estatus);
CREATE INDEX idx_cliente_nombre ON rentas_cliente(nombre);
```

Ejecutar:
```bash
python manage.py dbshell < add_indexes.sql
```

### **2. Configuración de PostgreSQL**

Edita `/etc/postgresql/15/main/postgresql.conf`:

```conf
# Memoria
shared_buffers = 256MB
effective_cache_size = 1GB
maintenance_work_mem = 64MB
work_mem = 16MB

# Conexiones
max_connections = 100

# Logging
log_statement = 'mod'
log_duration = on
log_min_duration_statement = 1000
```

Reiniciar PostgreSQL:
```bash
sudo systemctl restart postgresql
```

---

## 🔐 Seguridad PostgreSQL

### **1. Configurar pg_hba.conf**

Edita `/etc/postgresql/15/main/pg_hba.conf`:

```conf
# Conexiones locales
local   all             all                                     peer
host    all             all             127.0.0.1/32            scram-sha-256
host    all             all             ::1/128                 scram-sha-256

# Conexiones remotas (solo si es necesario)
host    nicancilweb_db  nicancil_user   192.168.1.0/24         scram-sha-256
```

### **2. Backup Automático**

Crea script `backup_db.sh`:

```bash
#!/bin/bash
BACKUP_DIR="/var/backups/nicancilweb"
DATE=$(date +%Y%m%d_%H%M%S)
DB_NAME="nicancilweb_db"
DB_USER="nicancil_user"

mkdir -p $BACKUP_DIR

# Backup
pg_dump -U $DB_USER -F c -b -v -f "$BACKUP_DIR/backup_$DATE.dump" $DB_NAME

# Mantener solo últimos 7 días
find $BACKUP_DIR -name "backup_*.dump" -mtime +7 -delete

echo "Backup completado: backup_$DATE.dump"
```

Hacer ejecutable y programar:
```bash
chmod +x backup_db.sh

# Agregar a crontab (diario a las 2 AM)
crontab -e
0 2 * * * /ruta/a/backup_db.sh
```

---

## 🐳 Docker con PostgreSQL (Opcional)

Si prefieres usar Docker para desarrollo:

```yaml
# docker-compose.yml
version: '3.8'

services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: nicancilweb_db
      POSTGRES_USER: nicancil_user
      POSTGRES_PASSWORD: desarrollo123
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

Ejecutar:
```bash
docker-compose up -d
DATABASE_URL=postgresql://nicancil_user:desarrollo123@localhost:5432/nicancilweb_db
python manage.py migrate
```

---

## 🆘 Solución de Problemas

### **Error: "FATAL: Peer authentication failed"**
```bash
# Cambiar método de autenticación en pg_hba.conf
sudo nano /etc/postgresql/15/main/pg_hba.conf
# Cambiar "peer" por "md5" o "scram-sha-256"
sudo systemctl restart postgresql
```

### **Error: "could not connect to server"**
```bash
# Verificar que PostgreSQL está corriendo
sudo systemctl status postgresql

# Iniciar si está detenido
sudo systemctl start postgresql
```

### **Error: "database does not exist"**
```bash
# Crear la base de datos
sudo -u postgres createdb nicancilweb_db
```

### **Error: "role does not exist"**
```bash
# Crear el usuario
sudo -u postgres createuser nicancil_user
```

---

## 📚 Recursos Adicionales

- [Documentación Django + PostgreSQL](https://docs.djangoproject.com/en/stable/ref/databases/#postgresql-notes)
- [PostgreSQL Performance Tuning](https://wiki.postgresql.org/wiki/Performance_Optimization)
- [Backup y Restore PostgreSQL](https://www.postgresql.org/docs/current/backup.html)

---

## ✅ Checklist de Producción

- [ ] PostgreSQL instalado y configurado
- [ ] Base de datos y usuario creados
- [ ] DATABASE_URL configurado en .env
- [ ] Migraciones ejecutadas
- [ ] Índices creados
- [ ] Backup automático configurado
- [ ] Conexión verificada
- [ ] Performance testeado

---

**¡Tu proyecto ahora está listo para usar PostgreSQL en producción!** 🚀
