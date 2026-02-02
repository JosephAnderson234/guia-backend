-- Script SQL: Datos de Prueba para Sistema de Citas de Fisioterapia
-- Ejecutar después de crear las tablas principales

-- ============================================================
-- 1. FISIOTERAPEUTAS
-- ============================================================
INSERT INTO fisioterapeutas (id, nombre) VALUES
(1, 'Dr. Carlos García'),
(2, 'Dra. María López'),
(3, 'Dr. Juan Martínez'),
(4, 'Dra. Ana Rodríguez'),
(5, 'Dr. Pedro Fernández')
ON CONFLICT (id) DO NOTHING;

-- Reiniciar secuencia
SELECT setval('fisioterapeutas_id_seq', (SELECT MAX(id) FROM fisioterapeutas));


-- ============================================================
-- 2. ESPACIOS (9 espacios físicos)
-- ============================================================
INSERT INTO espacios (id, nombre) VALUES
(1, 'Espacio 1 '),
(2, 'Espacio 2 '),
(3, 'Espacio 3 '),
(4, 'Espacio 4 '),
(5, 'Espacio 5 '),
(6, 'Espacio 6 '),
(7, 'Espacio 7 '),
(8, 'Espacio 8 '),
(9, 'Espacio 9 ')
ON CONFLICT (id) DO NOTHING;

-- Reiniciar secuencia
SELECT setval('espacios_id_seq', (SELECT MAX(id) FROM espacios));


-- ============================================================
-- 3. BLOQUES HORARIOS (Sesiones de 40 minutos)
-- ============================================================
INSERT INTO bloques_horarios (id, hora_inicio, hora_fin) VALUES
(1, '08:00:00', '08:40:00'),
(2, '09:00:00', '09:40:00'),
(3, '10:00:00', '10:40:00'),
(4, '11:00:00', '11:40:00'),
(5, '12:00:00', '12:40:00'),
(6, '14:00:00', '14:40:00'),
(7, '15:00:00', '15:40:00'),
(8, '16:00:00', '16:40:00'),
(9, '17:00:00', '17:40:00'),
(10, '18:00:00', '18:40:00')
ON CONFLICT (id) DO NOTHING;

-- Reiniciar secuencia
SELECT setval('bloques_horarios_id_seq', (SELECT MAX(id) FROM bloques_horarios));


-- ============================================================
-- 4. MÁQUINAS (3 máquinas para tratamiento específico)
-- ============================================================
INSERT INTO maquinas (id, codigo) VALUES
(1, 'MAG-001'),
(2, 'MAG-002'),
(3, 'MAG-003')
ON CONFLICT (id) DO NOTHING;

-- Reiniciar secuencia
SELECT setval('maquinas_id_seq', (SELECT MAX(id) FROM maquinas));


-- ============================================================
-- 5. PACIENTES (Casos de prueba variados)
-- ============================================================
INSERT INTO pacientes (
    id, 
    nombre, 
    telefono, 
    fecha_nacimiento, 
    centro_terapia_id, 
    usa_magneto, 
    requiere_tratamiento_especial, 
    seguro_medico, 
    aseguradora
) VALUES
-- Paciente normal sin máquina
(1, 'Juan Pérez', 987654321, '1985-05-15', 1, FALSE, FALSE, TRUE, 'Seguros Unidos'),

-- Paciente con máquina
(2, 'María González', 987654322, '1990-08-20', 1, TRUE, FALSE, TRUE, 'Salud Plus'),

-- Paciente con trato especial (sin máquina)
(3, 'Carlos Ruiz', 987654323, '1978-03-10', 1, FALSE, TRUE, FALSE, NULL),

-- Paciente con trato especial Y máquina
(4, 'Ana Martínez', 987654324, '1995-12-05', 1, TRUE, TRUE, TRUE, 'Cobertura Total'),

-- Paciente normal sin seguro
(5, 'Luis Torres', 987654325, '1982-07-22', 1, FALSE, FALSE, FALSE, NULL),

-- Paciente anciano con máquina
(6, 'Roberto Sánchez', 987654326, '1955-11-30', 1, TRUE, FALSE, TRUE, 'Tercera Edad Seguros'),

-- Paciente joven sin máquina
(7, 'Laura Ramírez', 987654327, '2000-02-14', 1, FALSE, FALSE, TRUE, 'Joven Salud'),

-- Paciente VIP con trato especial
(8, 'Isabel Vargas', 987654328, '1970-09-08', 1, FALSE, TRUE, TRUE, 'Premium Health'),

-- Paciente normal con máquina
(9, 'Diego Castro', 987654329, '1988-04-18', 1, TRUE, FALSE, TRUE, 'Salud Integral'),

-- Paciente sin datos completos
(10, 'Sofia Morales', NULL, NULL, 1, FALSE, FALSE, FALSE, NULL)

ON CONFLICT (id) DO NOTHING;

-- Reiniciar secuencia
SELECT setval('pacientes_id_seq', (SELECT MAX(id) FROM pacientes));


-- ============================================================
-- 6. DIAGNÓSTICOS (Opcional, para contexto)
-- ============================================================
INSERT INTO diagnosticos (id, paciente_id, sessions, treatment) VALUES
(1, 1, 10, 'Rehabilitación de rodilla post-operatoria'),
(2, 2, 15, 'Tratamiento con magnetoterapia para lumbalgia'),
(3, 3, 20, 'Terapia intensiva post-accidente'),
(4, 4, 12, 'Tratamiento especial con magnetoterapia'),
(5, 5, 8, 'Terapia para dolor cervical'),
(6, 6, 18, 'Rehabilitación geriátrica con magneto'),
(7, 7, 6, 'Prevención de lesiones deportivas'),
(8, 8, 25, 'Tratamiento VIP post-cirugía mayor'),
(9, 9, 12, 'Terapia con magnetoterapia para artritis'),
(10, 10, 5, 'Evaluación inicial')
ON CONFLICT (id) DO NOTHING;

-- Reiniciar secuencia
SELECT setval('diagnosticos_id_seq', (SELECT MAX(id) FROM diagnosticos));


-- ============================================================
-- 7. RESERVAS INICIALES (Opcional, para probar conflictos)
-- ============================================================

-- Reserva 1: Paciente normal en Espacio 1, Bloque 2 (09:00-09:40), 2026-02-10
INSERT INTO reservas (paciente_id, fisioterapeuta_id, espacio_id, bloque_id, maquina_id, fecha) VALUES
(1, 1, 1, 2, NULL, '2026-02-10');

-- Reserva 2: Paciente con máquina en Espacio 2, Bloque 2, 2026-02-10
INSERT INTO reservas (paciente_id, fisioterapeuta_id, espacio_id, bloque_id, maquina_id, fecha) VALUES
(2, 2, 2, 2, 1, '2026-02-10');

-- Reserva 3: Paciente con trato especial (ocupa completamente al fisio 3)
INSERT INTO reservas (paciente_id, fisioterapeuta_id, espacio_id, bloque_id, maquina_id, fecha) VALUES
(3, 3, 3, 2, NULL, '2026-02-10');

-- Reserva 4: Otro paciente normal
INSERT INTO reservas (paciente_id, fisioterapeuta_id, espacio_id, bloque_id, maquina_id, fecha) VALUES
(5, 1, 4, 2, NULL, '2026-02-10');


-- ============================================================
-- 8. VERIFICACIÓN DE DATOS
-- ============================================================

-- Contar registros
SELECT 
    (SELECT COUNT(*) FROM fisioterapeutas) AS total_fisioterapeutas,
    (SELECT COUNT(*) FROM espacios) AS total_espacios,
    (SELECT COUNT(*) FROM bloques_horarios) AS total_bloques,
    (SELECT COUNT(*) FROM maquinas) AS total_maquinas,
    (SELECT COUNT(*) FROM pacientes) AS total_pacientes,
    (SELECT COUNT(*) FROM diagnosticos) AS total_diagnosticos,
    (SELECT COUNT(*) FROM reservas) AS total_reservas;


-- Mostrar pacientes con características especiales
SELECT 
    id,
    nombre,
    usa_magneto,
    requiere_tratamiento_especial,
    CASE 
        WHEN usa_magneto AND requiere_tratamiento_especial THEN '🔴 Trato Especial + Máquina'
        WHEN requiere_tratamiento_especial THEN '🟡 Solo Trato Especial'
        WHEN usa_magneto THEN '🔵 Solo Máquina'
        ELSE '⚪ Normal'
    END AS categoria
FROM pacientes
ORDER BY id;


-- Mostrar reservas actuales
SELECT 
    r.id AS reserva_id,
    r.fecha,
    b.hora_inicio,
    b.hora_fin,
    p.nombre AS paciente,
    f.nombre AS fisioterapeuta,
    e.nombre AS espacio,
    CASE WHEN r.maquina_id IS NOT NULL THEN '✓' ELSE '✗' END AS usa_maquina
FROM reservas r
JOIN pacientes p ON r.paciente_id = p.id
JOIN fisioterapeutas f ON r.fisioterapeuta_id = f.id
JOIN espacios e ON r.espacio_id = e.id
JOIN bloques_horarios b ON r.bloque_id = b.id
ORDER BY r.fecha, b.hora_inicio;


-- ============================================================
-- SCRIPT COMPLETADO
-- ============================================================
-- Total de registros insertados:
-- - 5 Fisioterapeutas
-- - 9 Espacios
-- - 10 Bloques Horarios
-- - 3 Máquinas
-- - 10 Pacientes
-- - 10 Diagnósticos
-- - 4 Reservas iniciales
-- ============================================================
