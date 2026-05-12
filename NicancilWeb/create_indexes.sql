-- Índices para optimizar performance en PostgreSQL
-- Ejecutar: python manage.py dbshell < create_indexes.sql

-- Índices para tabla de Rentas
CREATE INDEX IF NOT EXISTS idx_renta_cliente ON rentas_renta(cliente_id);
CREATE INDEX IF NOT EXISTS idx_renta_estado ON rentas_renta(estado);
CREATE INDEX IF NOT EXISTS idx_renta_fecha_fin ON rentas_renta(fecha_fin);
CREATE INDEX IF NOT EXISTS idx_renta_fecha_inicio ON rentas_renta(fecha_inicio);
CREATE INDEX IF NOT EXISTS idx_renta_fecha_creacion ON rentas_renta(fecha_creacion);

-- Índices para tabla de Prendas
CREATE INDEX IF NOT EXISTS idx_prenda_tipo ON inventario_prenda(tipo);
CREATE INDEX IF NOT EXISTS idx_prenda_estatus ON inventario_prenda(estatus);
CREATE INDEX IF NOT EXISTS idx_prenda_genero ON inventario_prenda(genero);
CREATE INDEX IF NOT EXISTS idx_prenda_precio ON inventario_prenda(precio);

-- Índices para tabla de Clientes
CREATE INDEX IF NOT EXISTS idx_cliente_nombre ON rentas_cliente(nombre);
CREATE INDEX IF NOT EXISTS idx_cliente_telefono ON rentas_cliente(telefono);
CREATE INDEX IF NOT EXISTS idx_cliente_correo ON rentas_cliente(correo);

-- Índices para tabla de Variantes
CREATE INDEX IF NOT EXISTS idx_variante_prenda ON inventario_prendavariante(prenda_id);
CREATE INDEX IF NOT EXISTS idx_variante_estatus ON inventario_prendavariante(estatus);

-- Índices para tabla de Unidades
CREATE INDEX IF NOT EXISTS idx_unidad_variante ON inventario_prendaunidad(variante_id);
CREATE INDEX IF NOT EXISTS idx_unidad_estatus ON inventario_prendaunidad(estatus);
CREATE INDEX IF NOT EXISTS idx_unidad_numero_serie ON inventario_prendaunidad(numero_serie);

-- Índices para tabla de Citas
CREATE INDEX IF NOT EXISTS idx_cita_cliente ON citas_cita(cliente_id);
CREATE INDEX IF NOT EXISTS idx_cita_fecha ON citas_cita(fecha_cita);
CREATE INDEX IF NOT EXISTS idx_cita_estado ON citas_cita(estado);

-- Índices compuestos para consultas frecuentes
CREATE INDEX IF NOT EXISTS idx_renta_estado_fecha ON rentas_renta(estado, fecha_fin);
CREATE INDEX IF NOT EXISTS idx_prenda_tipo_estatus ON inventario_prenda(tipo, estatus);

-- Verificar índices creados
SELECT 
    tablename,
    indexname,
    indexdef
FROM 
    pg_indexes
WHERE 
    schemaname = 'public'
ORDER BY 
    tablename, indexname;
