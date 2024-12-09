from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Optional
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from database import SessionLocal
from models import User
import logging
import os
from sqlalchemy.exc import SQLAlchemyError

router = APIRouter()

# Схема OAuth2 для аутентификации по токену
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Конфигурация хэширования паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Конфигурация JWT
SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Логирование
logger = logging.getLogger(__name__)

# Pydantic модели для валидации данных
class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str
    employee_id: Optional[int] = None

class UserResponse(UserBase):
    pass

class UserLogin(BaseModel):
    username: str
    password: str

class PasswordChangeRequest(BaseModel):
    old_password: str
    new_password: str

# Функция для хэширования паролей
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# Функция для создания JWT токена доступа
def create_access_token(data: dict, expires_delta: timedelta) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Функция для проверки паролей
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Функция для аутентификации пользователей
def authenticate_user(username: str, password: str, db: Session) -> Optional[User]:
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

# Функция для получения сессии базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Функция для получения текущего аутентифицированного пользователя
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Невозможно проверить учетные данные",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    return user

# Эндпоинты для работы с пользователями

# Эндпоинт для регистрации нового пользователя
@router.post("/register/", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    logger.info(f"Регистрация пользователя: {user.username}")
    try:
        hashed_password = get_password_hash(user.password)
        db_user = User(username=user.username, email=user.email, hashed_password=hashed_password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        if user.employee_id:
            db_user.employee_id = user.employee_id
        db.commit()
        logger.info(f"Пользователь {user.username} успешно зарегистрирован")
        return db_user
    except Exception as e:
        logger.error(f"Ошибка при регистрации пользователя {user.username}: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Внутренняя ошибка сервера")

# Эндпоинт для входа пользователя и выдачи токена доступа
@router.post("/login/")
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    logger.info(f"Вход пользователя: {user.username}")
    db_user = authenticate_user(user.username, user.password, db)
    if not db_user:
        logger.warning(f"Неверные учетные данные для пользователя {user.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверные учетные данные",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": db_user.username}, expires_delta=access_token_expires)
    logger.info(f"Пользователь {user.username} успешно вошел в систему")
    return {"access_token": access_token, "token_type": "bearer"}

@router.put("/change-password/{user_id}")
def change_password(
    user_id: int,
    request: PasswordChangeRequest,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        logger.warning(f"Пользователь с ID={user_id} не найден")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден"
        )
    
    if not verify_password(request.old_password, user.hashed_password):
        logger.warning(f"Неверный старый пароль для пользователя с ID={user_id}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный старый пароль"
        )
    
    if len(request.new_password) < 6:
        logger.warning(f"Пароль для пользователя с ID={user_id} слишком короткий")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Новый пароль слишком короткий. Минимальная длина - 6 символов"
        )
    
    hashed_new_password = get_password_hash(request.new_password)
    user.hashed_password = hashed_new_password
    db.commit()
    
    logger.info(f"Пароль для пользователя с ID={user_id} успешно изменен")
    return {"message": "Пароль успешно изменен"}
