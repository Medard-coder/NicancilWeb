# Sistema de Reportes de Ventas - NicancilWeb

## Descripción
Sistema completo de reportes de ventas que permite generar informes detallados sobre rentas y prendas agregadas en períodos específicos, con capacidad de descarga en formato PDF.

## Características Implementadas

### 📊 Dashboard de Reportes
- **Filtros por fecha**: Selecciona período específico para generar reportes
- **Estadísticas en tiempo real**: 
  - Total de rentas en el período
  - Ingresos totales generados
  - Número de prendas nuevas agregadas
  - Rentas activas vs finalizadas

### 📋 Visualización de Datos
- **Tabla de rentas detallada**: ID, cliente, fecha, estado y total
- **Lista de prendas nuevas**: Con imagen, precio y fecha de agregado
- **Indicadores visuales**: Estados con colores y badges

### 📄 Generación de PDF
- **Reporte completo en PDF** con:
  - Resumen de estadísticas generales
  - Tabla detallada de todas las rentas del período
  - Lista de prendas nuevas agregadas
  - Formato profesional con tablas y estilos

## Archivos Creados/Modificados

### Nuevos Archivos
1. `templates/rentas/reportes_ventas.html` - Template principal de reportes
2. `test_reportes.py` - Script de prueba del sistema
3. `REPORTES_README.md` - Este archivo de documentación

### Archivos Modificados
1. `rentas/views.py` - Agregadas vistas `reportes_ventas()` y `generar_reporte_pdf()`
2. `rentas/urls.py` - Agregadas URLs para reportes
3. `templates/base_dashboard.html` - Actualizado enlace de reportes en menú
4. `requirements.txt` - Agregadas dependencias `reportlab` y `django-extensions`

## Dependencias Agregadas
- `reportlab>=4.0.0` - Para generación de PDFs
- `django-extensions>=3.2.0` - Utilidades adicionales para Django

## Cómo Usar el Sistema

### 1. Acceder a Reportes
- Ve al menú lateral y haz clic en "Reportes"
- O navega directamente a: `http://localhost:8000/rentas/reportes/`

### 2. Filtrar por Fechas
- Selecciona "Fecha Inicio" y "Fecha Fin" 
- Haz clic en "Filtrar" para actualizar los datos
- Por defecto muestra los últimos 30 días

### 3. Descargar PDF
- Después de filtrar, haz clic en "Descargar PDF"
- El archivo se descargará automáticamente
- Nombre del archivo: `reporte_ventas_YYYYMMDD_YYYYMMDD.pdf`

## Estructura del Reporte PDF

### Sección 1: Resumen General
- Total de rentas
- Ingresos totales
- Prendas nuevas agregadas
- Rentas activas
- Rentas finalizadas

### Sección 2: Detalle de Rentas
- ID de renta
- Nombre del cliente
- Fecha de creación
- Estado actual
- Total de la renta

### Sección 3: Prendas Nuevas Agregadas
- Nombre de la prenda
- Tipo (traje, vestido, accesorio)
- Precio
- Fecha de agregado

## Funcionalidades Técnicas

### Backend (Django)
- Consultas optimizadas con filtros de fecha
- Agregaciones para estadísticas (Sum, Count)
- Generación de PDF en memoria con ReportLab
- Manejo de errores y validaciones

### Frontend (HTML/CSS/JS)
- Interfaz responsive con Bootstrap 5
- Filtros automáticos al cambiar fechas
- Indicador de carga al generar PDF
- Diseño moderno con gradientes y sombras

### Seguridad
- Solo usuarios admin pueden acceder a reportes
- Validación de fechas requeridas
- Sanitización de parámetros de entrada

## Pruebas
Ejecuta el script de prueba para verificar que todo funciona:
```bash
python test_reportes.py
```

## Próximas Mejoras Sugeridas
1. **Gráficos**: Agregar charts con Chart.js
2. **Exportar Excel**: Opción adicional de descarga
3. **Reportes programados**: Envío automático por email
4. **Más filtros**: Por cliente, tipo de prenda, estado
5. **Comparativas**: Reportes de períodos anteriores

## Soporte
El sistema está completamente funcional y listo para usar. Todas las dependencias están instaladas y las pruebas pasan correctamente.