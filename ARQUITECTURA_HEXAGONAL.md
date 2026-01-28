# Arquitectura Hexagonal - Sistema de Fisioterapia

## 📋 Descripción General

El sistema de fisioterapia ha sido refactorizado siguiendo la arquitectura hexagonal (también conocida como arquitectura de puertos y adaptadores). Esta arquitectura permite que el core del negocio sea completamente independiente de los detalles técnicos de implementación.

## 🏗️ Estructura de Carpetas

```
app/
├── domain/                    # CORE - Lógica de negocio pura
│   ├── entities/             # Entidades de dominio (dataclasses)
│   │   └── __init__.py       # Paciente, Reserva, Diagnostico, etc.
│   ├── ports/                # Puertos (interfaces/contratos)
│   │   └── __init__.py       # PacienteRepository, ReservaRepository, etc.
│   └── usecases/             # Casos de uso (lógica de aplicación)
│       └── __init__.py       # CrearPaciente, ObtenerReserva, etc.
│
├── adapters/                  # ADAPTADORES - Implementaciones concretas
│   ├── database/             # Adaptador de base de datos
│   │   └── __init__.py       # SQLAlchemy repositories implementations
│   ├── api/                  # Adaptador de API
│   │   └── routes/           # FastAPI routers
│   │       └── pacientes.py  # Endpoints REST de pacientes
│   └── external/             # Adaptadores externos (Google Calendar, etc.)
│
├── shared/                    # COMPARTIDO - Código reutilizable
│   ├── schemas/              # Pydantic DTOs (Data Transfer Objects)
│   │   └── __init__.py       # Validación de entrada/salida
│   ├── utils/                # Utilidades comunes
│   └── container.py          # Inyección de dependencias (DI)
│
├── db/                        # LEGACY - Sesión y configuración de DB
│   ├── session.py            # SQLAlchemy session factory
│   ├── base.py               # Declarative base para ORM
│   └── models.py             # Modelos ORM originales (deprecados)
│
├── routes/                    # LEGACY - Rutas antiguas
│   └── citas.py              # Endpoints de citas
│
└── main.py                    # Punto de entrada de FastAPI
```

## 🔄 Flujo de Datos

### Hexagonal Flow (Nuevo - Recomendado)

```
HTTP Request
    ↓
API Route Adapter (app/adapters/api/routes/pacientes.py)
    ↓
Use Case (app/domain/usecases)
    ↓
Domain Entity (app/domain/entities) ← Pura lógica de negocio
    ↓
Repository Port (app/domain/ports) ← Interfaz/contrato
    ↓
Repository Adapter (app/adapters/database) ← Implementación SQLAlchemy
    ↓
Database (SQLAlchemy ORM)
    ↓
HTTP Response (Pydantic Schema)
```

## 📚 Componentes Principales

### 1. Domain Layer (app/domain/)

**Entities** (`app/domain/entities/__init__.py`)
- Dataclasses puros sin dependencias externas
- Representan conceptos del negocio: Paciente, Reserva, Diagnostico, etc.
- Ejemplo:
```python
@dataclass
class Paciente:
    id: Optional[int] = None
    nombre: str
    telefono: Optional[int] = None
    fecha_nacimiento: Optional[date] = None
    seguro_medico: bool = False
    aseguradora: Optional[str] = None
    created_at: Optional[datetime] = None
```

**Ports** (`app/domain/ports/__init__.py`)
- Interfaces (ABC) que definen los contratos de los adaptadores
- Define qué operaciones DEBEN implementar los repositorios
- Ejemplo:
```python
class PacienteRepository(ABC):
    @abstractmethod
    async def crear(self, paciente: Paciente) -> Paciente: ...
    
    @abstractmethod
    async def obtener_por_id(self, id: int) -> Optional[Paciente]: ...
    
    @abstractmethod
    async def listar(self, skip: int, limit: int) -> List[Paciente]: ...
```

**Use Cases** (`app/domain/usecases/__init__.py`)
- Orquestación de la lógica de negocio
- Coordinan entre entidades y repositorios
- Ejemplo:
```python
class CrearPaciente:
    def __init__(self, repo: PacienteRepository):
        self.repo = repo
    
    async def ejecutar(self, datos: dict) -> Paciente:
        paciente = Paciente(**datos)
        return await self.repo.crear(paciente)
```

### 2. Adapters Layer (app/adapters/)

**Database Adapter** (`app/adapters/database/__init__.py`)
- Implementa los puertos (ports) usando SQLAlchemy
- Define modelos ORM (PacienteORM, ReservaORM, etc.)
- Implementa repositorios concretos (PacienteRepositoryImpl, etc.)
- Maneja la persistencia en BD

**API Adapter** (`app/adapters/api/routes/`)
- Implementa endpoints REST con FastAPI
- Recibe HTTP requests y los convierte en llamadas a use cases
- Convierte entidades de dominio a DTOs (Pydantic schemas)
- Ejemplo:
```python
@router.post("/", response_model=PacienteResponse)
async def crear_paciente(
    datos: PacienteCreate,
    repo: PacienteRepository = Depends(get_paciente_repo)
) -> PacienteResponse:
    use_case = CrearPaciente(repo)
    paciente = await use_case.ejecutar(datos.dict())
    return PacienteResponse.from_orm(paciente)
```

### 3. Shared Layer (app/shared/)

**Schemas** (`app/shared/schemas/__init__.py`)
- Pydantic models para validación de entrada/salida
- DTOs (Data Transfer Objects) para la API
- Ejemplo:
```python
class PacienteCreate(PacienteBase):
    pass

class PacienteResponse(PacienteBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True
```

**Container** (`app/shared/container.py`)
- Inyección de dependencias (DI)
- Inicializa repositorios y casos de uso
- Gestiona el ciclo de vida de las dependencias
- Ejemplo:
```python
container = Container(db_session)
paciente_repo = container.get_repository('paciente')
use_case = container.get_use_case('crear_paciente')
```

## 🎯 Ventajas de la Arquitectura Hexagonal

1. **Independencia de Framework**: El dominio no depende de FastAPI, SQLAlchemy, etc.
2. **Testabilidad**: Fácil de testear con mocks sin necesidad de BD real
3. **Mantenibilidad**: Cambios en un adaptador no afectan el dominio
4. **Escalabilidad**: Fácil agregar nuevos adaptadores (GraphQL, gRPC, eventos, etc.)
5. **Claridad**: Separación clara de responsabilidades
6. **DDD Ready**: Preparado para Domain-Driven Design

## 📊 Ejemplo: Crear un Paciente

### Paso 1: Request HTTP
```bash
POST /api/pacientes/
{
  "nombre": "Juan Pérez",
  "telefono": 3001234567,
  "seguro_medico": true,
  "aseguradora": "Salud Total"
}
```

### Paso 2: API Adapter (pacientes.py)
- FastAPI parsea el JSON a `PacienteCreate` (Pydantic schema)
- Inyecta el `PacienteRepository`
- Llama al use case

### Paso 3: Use Case (usecases)
- `CrearPaciente` recibe los datos
- Crea una entidad `Paciente` del dominio
- Llama al repositorio

### Paso 4: Domain Layer
- Entidad `Paciente` valida los datos
- Se ejecuta la lógica de negocio pura

### Paso 5: Database Adapter
- `PacienteRepositoryImpl` convierte la entidad a ORM
- SQLAlchemy persiste en la BD
- Retorna la entidad creada

### Paso 6: Response
- API adapter convierte a `PacienteResponse` (Pydantic)
- Retorna JSON al cliente

## 🔌 Agregar Nuevos Adaptadores

### Ejemplo: Adaptador de GraphQL

1. Crear `app/adapters/graphql/`
2. Definir esquemas GraphQL
3. Usar los mismos use cases del dominio
4. El dominio no cambia, solo agregamos un nuevo adaptador

```python
# app/adapters/graphql/queries.py
class Query:
    @strawberry.field
    async def pacientes(self) -> List[PacienteType]:
        repo = PacienteRepositoryImpl(db)
        use_case = ListarPacientes(repo)
        return await use_case.ejecutar(0, 10)
```

## 📝 Próximos Pasos

1. **Completar Adaptadores de BD**: Implementar ReservaRepositoryImpl, DiagnosticoRepositoryImpl, etc.
2. **Completar Rutas API**: Crear endpoints para Reservas, Diagnosticos, etc.
3. **Tests**: Agregar pruebas unitarias y de integración
4. **Validación**: Agregar reglas de negocio más complejas en use cases
5. **Eventos**: Implementar eventos de dominio (DomainEvents)
6. **Logging**: Agregar logging estructurado en cada capa

## 🎓 Referencias

- [Arquitectura Hexagonal - Alistair Cockburn](https://alistair.cockburn.us/hexagonal-architecture/)
- [Puertos y Adaptadores](https://github.com/aaronshaf/hexagonal-architecture)
- [FastAPI Dependency Injection](https://fastapi.tiangolo.com/tutorial/dependencies/)
- [SQLAlchemy Best Practices](https://docs.sqlalchemy.org/en/20/orm/quickstart.html)

## ✅ Checklist de Implementación

- [x] Dominio definido (entities, ports, usecases)
- [x] Adaptador de BD parcialmente implementado (Paciente)
- [x] Adaptador de API parcialmente implementado (Paciente)
- [x] Contenedor DI creado
- [x] Main.py integrado
- [ ] Completar adaptadores de BD (Reserva, Diagnostico, etc.)
- [ ] Completar rutas API (Reserva, Diagnostico, etc.)
- [ ] Tests unitarios
- [ ] Tests de integración
- [ ] Documentación Swagger/OpenAPI
- [ ] Migración de datos de BD anterior

---

**Versión**: 2.0.0 (Hexagonal)  
**Última actualización**: 2024
