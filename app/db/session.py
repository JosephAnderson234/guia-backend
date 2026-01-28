from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.db.config import DATABASE_URL, SQLALCHEMY_ECHO, SQLALCHEMY_POOL_SIZE, SQLALCHEMY_MAX_OVERFLOW

# PostgreSQL Engine
engine = create_engine(
    DATABASE_URL,
    echo=SQLALCHEMY_ECHO,
    pool_size=SQLALCHEMY_POOL_SIZE,
    max_overflow=SQLALCHEMY_MAX_OVERFLOW,
    pool_pre_ping=True,  # Verifica conexiones antes de usarlas
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False
)

def get_db() -> Session:
    """Obtener una sesión de base de datos"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
