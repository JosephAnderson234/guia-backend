"""
Script de Ejemplo: Cómo usar los endpoints de citas

Este archivo muestra ejemplos de requests para probar los endpoints implementados.
"""

import requests
from datetime import date, timedelta

# Configuración
BASE_URL = "http://localhost:8000"
API_CITAS = f"{BASE_URL}/api/citas"


def ejemplo_1_consultar_disponibilidad():
    """
    Ejemplo 1: Consultar disponibilidad para un rango de fechas
    """
    print("\n" + "="*60)
    print("EJEMPLO 1: Consultar Disponibilidad")
    print("="*60)
    
    # Parámetros
    fecha_inicio = date(2026, 2, 10)
    fecha_fin = date(2026, 2, 17)
    paciente_id = 5
    fisioterapeuta_id = 2
    
    # Request
    params = {
        "fecha_inicio": fecha_inicio.isoformat(),
        "fecha_fin": fecha_fin.isoformat(),
        "paciente_id": paciente_id,
        "fisioterapeuta_id": fisioterapeuta_id
    }
    
    print(f"\nGET {API_CITAS}/disponibles")
    print(f"Params: {params}")
    
    # Descomentar para ejecutar:
    # response = requests.get(f"{API_CITAS}/disponibles", params=params)
    # print(f"\nStatus Code: {response.status_code}")
    # print(f"Response:\n{response.json()}")


def ejemplo_2_agendar_tratamiento_exitoso():
    """
    Ejemplo 2: Agendar tratamiento recurrente (caso exitoso)
    """
    print("\n" + "="*60)
    print("EJEMPLO 2: Agendar Tratamiento (Éxito)")
    print("="*60)
    
    # Request body
    data = {
        "paciente_id": 5,
        "fisioterapeuta_id": 3,
        "bloque_id": 2,
        "fecha_inicio": "2026-02-10",
        "total_sesiones": 9,
        "requiere_maquina": True
    }
    
    print(f"\nPOST {API_CITAS}/agendar")
    print(f"Body: {data}")
    
    # Descomentar para ejecutar:
    # response = requests.post(f"{API_CITAS}/agendar", json=data)
    # print(f"\nStatus Code: {response.status_code}")
    # print(f"Response:\n{response.json()}")


def ejemplo_3_agendar_sin_maquina():
    """
    Ejemplo 3: Agendar tratamiento sin máquina
    """
    print("\n" + "="*60)
    print("EJEMPLO 3: Agendar Tratamiento (Sin Máquina)")
    print("="*60)
    
    # Request body
    data = {
        "paciente_id": 8,
        "fisioterapeuta_id": 2,
        "bloque_id": 5,
        "fecha_inicio": "2026-02-15",
        "total_sesiones": 6,
        "requiere_maquina": False
    }
    
    print(f"\nPOST {API_CITAS}/agendar")
    print(f"Body: {data}")
    
    # Descomentar para ejecutar:
    # response = requests.post(f"{API_CITAS}/agendar", json=data)
    # print(f"\nStatus Code: {response.status_code}")
    # if response.status_code == 200:
    #     result = response.json()
    #     print(f"✅ Sesiones agendadas: {result['total_sesiones_agendadas']}")
    #     print(f"Mensaje: {result['mensaje']}")
    # else:
    #     print(f"❌ Error: {response.json()['detail']}")


def ejemplo_4_consultar_disponibilidad_simple():
    """
    Ejemplo 4: Consultar disponibilidad sin filtros
    """
    print("\n" + "="*60)
    print("EJEMPLO 4: Consultar Disponibilidad (Sin Filtros)")
    print("="*60)
    
    # Solo fechas, sin filtros de paciente/fisioterapeuta
    params = {
        "fecha_inicio": "2026-02-10",
        "fecha_fin": "2026-02-11"
    }
    
    print(f"\nGET {API_CITAS}/disponibles")
    print(f"Params: {params}")
    
    # Descomentar para ejecutar:
    # response = requests.get(f"{API_CITAS}/disponibles", params=params)
    # print(f"\nStatus Code: {response.status_code}")
    # if response.status_code == 200:
    #     result = response.json()
    #     print(f"✅ Bloques disponibles: {result['total_bloques']}")
    #     for bloque in result['bloques_disponibles'][:3]:  # Mostrar solo 3
    #         print(f"  - Fecha: {bloque['fecha']}, Bloque: {bloque['bloque_id']}, "
    #               f"Espacios: {bloque['espacios_disponibles']}")


def ejemplo_5_datos_curl():
    """
    Ejemplo 5: Comandos cURL para probar desde terminal
    """
    print("\n" + "="*60)
    print("EJEMPLO 5: Comandos cURL")
    print("="*60)
    
    print("\n--- Consultar Disponibilidad ---")
    print("""
curl -X GET "http://localhost:8000/api/citas/disponibles?fecha_inicio=2026-02-10&fecha_fin=2026-02-17&paciente_id=5" \\
  -H "Accept: application/json"
""")
    
    print("\n--- Agendar Tratamiento ---")
    print("""
curl -X POST "http://localhost:8000/api/citas/agendar" \\
  -H "Content-Type: application/json" \\
  -d '{
    "paciente_id": 5,
    "fisioterapeuta_id": 3,
    "bloque_id": 2,
    "fecha_inicio": "2026-02-10",
    "total_sesiones": 9,
    "requiere_maquina": true
  }'
""")


def verificar_datos_necesarios():
    """
    Lista de datos que deben existir en la BD antes de probar
    """
    print("\n" + "="*60)
    print("DATOS NECESARIOS EN BASE DE DATOS")
    print("="*60)
    
    print("""
Antes de probar los endpoints, asegúrate de tener:

1. PACIENTES (tabla: pacientes)
   - Al menos 5 pacientes registrados
   - Algunos con usa_magneto = True
   - Algunos con requiere_tratamiento_especial = True

2. FISIOTERAPEUTAS (tabla: fisioterapeutas)
   - Al menos 3 fisioterapeutas registrados
   - Ejemplo: INSERT INTO fisioterapeutas (nombre) VALUES ('Dr. García'), ('Dra. López'), ('Dr. Martínez');

3. ESPACIOS (tabla: espacios)
   - 9 espacios registrados
   - Ejemplo: INSERT INTO espacios (nombre) VALUES ('Espacio 1'), ('Espacio 2'), ... ('Espacio 9');

4. BLOQUES HORARIOS (tabla: bloques_horarios)
   - Bloques de 40 minutos
   - Ejemplo:
     INSERT INTO bloques_horarios (hora_inicio, hora_fin) VALUES
     ('08:00', '08:40'),
     ('09:00', '09:40'),
     ('10:00', '10:40'),
     ('11:00', '11:40'),
     ('14:00', '14:40'),
     ('15:00', '15:40');

5. MÁQUINAS (tabla: maquinas)
   - 3 máquinas registradas
   - Ejemplo: INSERT INTO maquinas (codigo) VALUES ('MAQ-001'), ('MAQ-002'), ('MAQ-003');

SCRIPTS SQL:
Revisa los archivos:
- init_db.py (para inicializar la BD)
- test_postgresql.py (para verificar conexión)
""")


def main():
    """
    Ejecutar todos los ejemplos
    """
    print("\n")
    print("╔" + "="*58 + "╗")
    print("║" + " "*10 + "EJEMPLOS DE USO - ENDPOINTS DE CITAS" + " "*11 + "║")
    print("╚" + "="*58 + "╝")
    
    verificar_datos_necesarios()
    ejemplo_1_consultar_disponibilidad()
    ejemplo_2_agendar_tratamiento_exitoso()
    ejemplo_3_agendar_sin_maquina()
    ejemplo_4_consultar_disponibilidad_simple()
    ejemplo_5_datos_curl()
    
    print("\n" + "="*60)
    print("NOTA: Descomenta los requests.get/post para ejecutar")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
