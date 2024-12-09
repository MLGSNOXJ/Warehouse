from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import create_tables  # Импорт базы данных и функций для создания таблиц
import logging
from users import router as users_router
from employees import router as employees_router
from products import router as products_router
from cart import router as cart_router


# Инициализация FastAPI приложения
app = FastAPI()

# Создание таблиц базы данных, если они не существуют
create_tables()

# Разрешенные источники для CORS
origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://127.0.0.1",
    "http://127.0.0.1:8080",
]

# Добавление CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Разрешенные источники
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Подключение роутеров
app.include_router(users_router, prefix="/users", tags=["Users"])
app.include_router(employees_router, prefix="/employees", tags=["Employees"])
app.include_router(products_router, prefix="/products", tags=["Products"])
app.include_router(cart_router, prefix="/api", tags=["Cart"])