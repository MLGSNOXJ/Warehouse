from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from base_class import Base  # импортируем Base из нового модуля

# URL подключения к базе данных PostgreSQL
URL_DATABASE = 'postgresql://postgres:artem20041945@localhost:5432/MyDatabase'

# Создание движка для взаимодействия с базой данных
engine = create_engine(URL_DATABASE)

# Создание сессии базы данных
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Функция для создания всех таблиц, определённых в моделях SQLAlchemy
def create_tables():
    import models
    Base.metadata.create_all(bind=engine)

