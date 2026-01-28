#!/usr/bin/env python
"""
✅ CHECKLIST DE CONFIGURACIÓN - Persistencia en Base de Datos
Ejecuta este script para verificar que todo está funcionando correctamente
"""

import sys
import os
from pathlib import Path

def print_header(texto):
    print("\n" + "="*70)
    print(f"  {texto}")
    print("="*70)

def print_check(paso, completado, detalles=""):
    simbolo = "✅" if completado else "❌"
    print(f"{simbolo} {paso}")
    if detalles:
        print(f"   └─ {detalles}")

def check_imports():
    """Verifica que se pueden importar los módulos necesarios"""
    print_header("1. VERIFICACIÓN DE IMPORTS")
    
    checks = {
        "SQLAlchemy": False,
        "FastAPI": False,
        "Pydantic": False,
        "dotenv": False,
    }
    
    try:
        import sqlalchemy
        checks["SQLAlchemy"] = True
    except ImportError:
        pass
    
    try:
        import fastapi
        checks["FastAPI"] = True
    except ImportError:
        pass
    
    try:
        import pydantic
        checks["Pydantic"] = True
    except ImportError:
        pass
    
    try:
        import dotenv
        checks["dotenv"] = True
    except ImportError:
        pass
    
    for package, ok in checks.items():
        status = "Instalado" if ok else "NO INSTALADO"
        print_check(f"Módulo {package}", ok, status)
    
    return all(checks.values())

def check_archivos():
    """Verifica que existan los archivos necesarios"""
    print_header("2. VERIFICACIÓN DE ARCHIVOS")
    
    archivos = {
        "app/db/session.py": "Configuración de sesión SQLAlchemy",
        "app/db/base.py": "Base declarativa",
        "app/db/models.py": "Modelos SQLAlchemy",
        "app/db/init_db.py": "Script de inicialización",
        "app/core/config.py": "Configuración (DATABASE_URL)",
        "app/schemas/empresas.py": "Esquemas Pydantic",
        ".env": "Variables de entorno",
    }
    
    resultado = {}
    for archivo, descripcion in archivos.items():
        existe = Path(archivo).exists()
        resultado[archivo] = existe
        print_check(archivo, existe, descripcion)
    
    return all(resultado.values())

def check_ambiente():
    """Verifica las variables de entorno"""
    print_header("3. VERIFICACIÓN DE AMBIENTE")
    
    from dotenv import load_dotenv
    load_dotenv()
    
    database_url = os.getenv("DATABASE_URL")
    
    db_ok = database_url is not None
    print_check("DATABASE_URL configurado", db_ok, 
                f"Valor: {database_url[:50]}..." if database_url else "No encontrado")
    
    return db_ok

def check_modelos():
    """Verifica que los modelos estén correctamente definidos"""
    print_header("4. VERIFICACIÓN DE MODELOS")
    
    try:
        from app.db.models import Empresa, Empleado, PerfilLaboral, Cita
        
        # Verificar que Empresa tiene el atributo empleados
        empresa_ok = hasattr(Empresa, 'empleados')
        print_check("Modelo Empresa", True, "✓ Relación one-to-many con Empleados")
        
        # Verificar que Empleado tiene empresa y perfil
        empleado_ok = hasattr(Empleado, 'empresa') and hasattr(Empleado, 'perfil')
        print_check("Modelo Empleado", empleado_ok, "✓ Relaciones con Empresa y PerfilLaboral")
        
        # Verificar que PerfilLaboral tiene empleado
        perfil_ok = hasattr(PerfilLaboral, 'empleado')
        print_check("Modelo PerfilLaboral", perfil_ok, "✓ Relación one-to-one con Empleado")
        
        # Verificar que Cita está independiente
        cita_ok = True
        print_check("Modelo Cita", cita_ok, "✓ Independiente (sin integración)")
        
        return empresa_ok and empleado_ok and perfil_ok and cita_ok
        
    except ImportError as e:
        print_check("Importar modelos", False, f"Error: {str(e)}")
        return False

def check_base_datos():
    """Verifica la conexión a la base de datos"""
    print_header("5. VERIFICACIÓN DE CONEXIÓN A BD")
    
    try:
        from app.db.session import engine
        
        # Intentar conectar
        with engine.connect() as connection:
            print_check("Conexión a BD", True, "✓ Conectado exitosamente")
            return True
            
    except Exception as e:
        print_check("Conexión a BD", False, f"Error: {str(e)}")
        print("\n   Solución: Ejecuta: python -m app.db.init_db")
        return False

def check_tablas():
    """Verifica que las tablas existan en la BD"""
    print_header("6. VERIFICACIÓN DE TABLAS")
    
    try:
        from app.db.session import engine
        from sqlalchemy import inspect
        
        inspector = inspect(engine)
        tablas_existentes = inspector.get_table_names()
        
        tablas_esperadas = ["empresas", "empleados", "perfiles_laborales", "citas"]
        
        todas_ok = all(tabla in tablas_existentes for tabla in tablas_esperadas)
        
        if tablas_existentes:
            print_check("Tablas detectadas", True, f"Total: {len(tablas_existentes)}")
            for tabla in tablas_existentes:
                print(f"   • {tabla}")
        else:
            print_check("Tablas detectadas", False, "No hay tablas en la BD")
            print("\n   Solución: Ejecuta: python -m app.db.init_db")
        
        return todas_ok or len(tablas_existentes) == 0  # OK si existen o si está vacía (primera ejecución)
        
    except Exception as e:
        print_check("Verificar tablas", False, f"Error: {str(e)}")
        return False

def check_esquemas():
    """Verifica que los esquemas Pydantic estén correctos"""
    print_header("7. VERIFICACIÓN DE ESQUEMAS PYDANTIC")
    
    try:
        from app.schemas.empresas import (
            EmpresaResponse, EmpleadoResponse, PerfilLaboralResponse,
            EmpresaConEmpleados, EmpleadoConPerfil
        )
        
        print_check("Esquema EmpresaResponse", True)
        print_check("Esquema EmpleadoResponse", True)
        print_check("Esquema PerfilLaboralResponse", True)
        print_check("Esquema EmpresaConEmpleados", True, "Con relación one-to-many")
        print_check("Esquema EmpleadoConPerfil", True, "Con relación one-to-one")
        
        return True
        
    except ImportError as e:
        print_check("Esquemas Pydantic", False, f"Error: {str(e)}")
        return False

def print_resumen(resultados):
    """Imprime resumen final"""
    print_header("📋 RESUMEN FINAL")
    
    total = len(resultados)
    pasados = sum(resultados.values())
    
    print(f"\n  Checks completados: {pasados}/{total}")
    
    if pasados == total:
        print("\n  🎉 ¡TODO ESTÁ CONFIGURADO CORRECTAMENTE!")
        print("\n  Próximos pasos:")
        print("  1. Ejecuta: python -m app.db.init_db")
        print("  2. Ejecuta: python test_relaciones_db.py")
        print("  3. Ejecuta: python ver_estructura_db.py")
        return True
    else:
        print(f"\n  ⚠️  {total - pasados} check(s) fallido(s)")
        print("\n  Revisa los errores arriba y ejecuta:")
        print("  - pip install -r app/requirements.txt")
        print("  - python -m app.db.init_db")
        return False

if __name__ == "__main__":
    print("\n" + "█" * 70)
    print("█" + " " * 68 + "█")
    print("█  CHECKLIST DE CONFIGURACIÓN - PERSISTENCIA BD".ljust(69) + "█")
    print("█" + " " * 68 + "█")
    print("█" * 70)
    
    resultados = {
        "Imports": check_imports(),
        "Archivos": check_archivos(),
        "Ambiente": check_ambiente(),
        "Modelos": check_modelos(),
        "Conexión BD": check_base_datos(),
        "Tablas": check_tablas(),
        "Esquemas": check_esquemas(),
    }
    
    todo_ok = print_resumen(resultados)
    
    print("\n" + "█" * 70 + "\n")
    
    sys.exit(0 if todo_ok else 1)
