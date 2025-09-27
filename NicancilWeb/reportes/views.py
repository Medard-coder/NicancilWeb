from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db.models import Sum
from django.utils import timezone
from datetime import datetime, timedelta
from rentas.models import Renta, Cliente
from inventario.models import Prenda

def reportes_ventas(request):
    """Vista principal para generar reportes de ventas"""
    # Obtener fechas por defecto (último mes)
    fecha_fin = timezone.now().date()
    fecha_inicio = fecha_fin - timedelta(days=30)
    
    # Si hay filtros en la request
    if request.GET.get('fecha_inicio'):
        fecha_inicio = datetime.strptime(request.GET.get('fecha_inicio'), '%Y-%m-%d').date()
    if request.GET.get('fecha_fin'):
        fecha_fin = datetime.strptime(request.GET.get('fecha_fin'), '%Y-%m-%d').date()
    
    # Estadísticas de rentas
    rentas_periodo = Renta.objects.filter(
        fecha_creacion__date__range=[fecha_inicio, fecha_fin]
    )
    
    # Estadísticas de prendas agregadas
    prendas_nuevas = Prenda.objects.filter(
        fecha_creacion__date__range=[fecha_inicio, fecha_fin]
    )
    
    # Resumen de estadísticas
    estadisticas = {
        'total_rentas': rentas_periodo.count(),
        'ingresos_totales': rentas_periodo.aggregate(Sum('precio_total'))['precio_total__sum'] or 0,
        'prendas_nuevas': prendas_nuevas.count(),
        'rentas_activas': rentas_periodo.filter(estado='activa').count(),
        'rentas_finalizadas': rentas_periodo.filter(estado='finalizada').count(),
    }
    
    return render(request, 'reportes/reportes_ventas.html', {
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin,
        'estadisticas': estadisticas,
        'rentas': rentas_periodo.order_by('-fecha_creacion'),
        'prendas_nuevas': prendas_nuevas.order_by('-fecha_creacion')
    })

def generar_reporte_pdf(request):
    """Generar reporte de ventas en PDF"""
    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.units import inch
    import io
    
    # Obtener parámetros de fecha
    fecha_inicio_str = request.GET.get('fecha_inicio')
    fecha_fin_str = request.GET.get('fecha_fin')
    
    if not fecha_inicio_str or not fecha_fin_str:
        return JsonResponse({'error': 'Fechas requeridas'}, status=400)
    
    fecha_inicio = datetime.strptime(fecha_inicio_str, '%Y-%m-%d').date()
    fecha_fin = datetime.strptime(fecha_fin_str, '%Y-%m-%d').date()
    
    # Crear el PDF en memoria
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []
    
    # Estilos
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=30,
        alignment=1  # Centrado
    )
    
    # Título
    title = Paragraph(f"Reporte de Ventas<br/>Del {fecha_inicio.strftime('%d/%m/%Y')} al {fecha_fin.strftime('%d/%m/%Y')}", title_style)
    elements.append(title)
    elements.append(Spacer(1, 20))
    
    # Obtener datos
    rentas_periodo = Renta.objects.filter(
        fecha_creacion__date__range=[fecha_inicio, fecha_fin]
    )
    
    prendas_nuevas = Prenda.objects.filter(
        fecha_creacion__date__range=[fecha_inicio, fecha_fin]
    )
    
    # Resumen estadísticas
    ingresos_totales = rentas_periodo.aggregate(Sum('precio_total'))['precio_total__sum'] or 0
    
    resumen_data = [
        ['Concepto', 'Cantidad'],
        ['Total de Rentas', str(rentas_periodo.count())],
        ['Ingresos Totales', f'${ingresos_totales:,.2f}'],
        ['Prendas Nuevas Agregadas', str(prendas_nuevas.count())],
        ['Rentas Activas', str(rentas_periodo.filter(estado='activa').count())],
        ['Rentas Finalizadas', str(rentas_periodo.filter(estado='finalizada').count())],
    ]
    
    resumen_table = Table(resumen_data, colWidths=[3*inch, 2*inch])
    resumen_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    elements.append(Paragraph("Resumen General", styles['Heading2']))
    elements.append(resumen_table)
    elements.append(Spacer(1, 30))
    
    # Detalle de rentas
    if rentas_periodo.exists():
        elements.append(Paragraph("Detalle de Rentas", styles['Heading2']))
        
        rentas_data = [['ID', 'Cliente', 'Fecha', 'Estado', 'Total']]
        for renta in rentas_periodo.order_by('-fecha_creacion'):
            rentas_data.append([
                str(renta.id),
                renta.cliente.nombre[:20],
                renta.fecha_creacion.strftime('%d/%m/%Y'),
                renta.get_estado_display(),
                f'${renta.precio_total:,.2f}'
            ])
        
        rentas_table = Table(rentas_data, colWidths=[0.8*inch, 2*inch, 1.2*inch, 1.5*inch, 1.2*inch])
        rentas_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 8)
        ]))
        
        elements.append(rentas_table)
        elements.append(Spacer(1, 30))
    
    # Detalle de prendas nuevas
    if prendas_nuevas.exists():
        elements.append(Paragraph("Prendas Nuevas Agregadas", styles['Heading2']))
        
        prendas_data = [['Nombre', 'Tipo', 'Precio', 'Fecha Agregada']]
        for prenda in prendas_nuevas.order_by('-fecha_creacion'):
            prendas_data.append([
                prenda.nombre[:25],
                prenda.get_tipo_display(),
                f'${prenda.precio:,.2f}',
                prenda.fecha_creacion.strftime('%d/%m/%Y')
            ])
        
        prendas_table = Table(prendas_data, colWidths=[2.5*inch, 1.5*inch, 1.2*inch, 1.5*inch])
        prendas_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 8)
        ]))
        
        elements.append(prendas_table)
    
    # Generar PDF
    doc.build(elements)
    
    # Preparar respuesta
    buffer.seek(0)
    response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
    filename = f'reporte_ventas_{fecha_inicio.strftime("%Y%m%d")}_{fecha_fin.strftime("%Y%m%d")}.pdf'
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    return response