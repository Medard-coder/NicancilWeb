# App Reportes - NicancilWeb

## Descripción
App independiente para generar reportes de ventas con datos de rentas y prendas agregadas, con capacidad de filtrado por fechas y descarga en PDF.

## Estructura de la App

### Archivos Principales
- `views.py` - Vistas para mostrar reportes y generar PDFs
- `urls.py` - URLs de la app reportes
- `templates/reportes/reportes_ventas.html` - Template principal

### Funcionalidades
1. **Dashboard de Reportes**: Visualización de estadísticas con filtros de fecha
2. **Generación de PDF**: Reportes descargables en formato profesional
3. **Datos Integrados**: Acceso a modelos de rentas e inventario

### URLs Disponibles
- `/reportes/` - Dashboard principal de reportes
- `/reportes/pdf/` - Generación y descarga de PDF

### Dependencias de Otras Apps
- `rentas.models` - Para datos de rentas y clientes
- `inventario.models` - Para datos de prendas

## Uso
La app está completamente integrada al sistema principal y accesible desde el menú "Reportes" en el dashboard.