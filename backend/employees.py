from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from typing import List, Optional
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Employee, User
from pydantic import BaseModel
import logging
import io
from fastapi.responses import StreamingResponse
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt  # Import jwt and JWTError
import os

router = APIRouter()

logger = logging.getLogger(__name__)

# OAuth2 scheme definition
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# JWT Configuration (Importing these values or setting them up)
SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")
ALGORITHM = "HS256"

# Pydantic модели для валидации данных
class EmployeeBase(BaseModel):
    FIO: str
    surname: str
    company_id: int
    post: str
    email: str
    phone: str

class EmployeeResponse(EmployeeBase):
    id: int
    company_id: Optional[int] = None
    email: Optional[str] = None
    phone: Optional[str] = None

    class Config:
        from_attributes = True

class EmployeeUpdate(BaseModel):
    FIO: str
    surname: str
    post: str
    email: str
    phone: str
    photo: Optional[bytes] = None

    class Config:
        from_attributes = True

class EmployeeCreate(BaseModel):
    FIO: str
    surname: str
    post: str

# Функция для получения сессии базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Функция для получения текущего аутентифицированного пользователя
def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> User:
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

@router.post("/", response_model=EmployeeResponse)
def create_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):
    try:
        db_employee = Employee(
            FIO=employee.FIO,
            surname=employee.surname,
            post=employee.post,
            # Убедитесь, что другие необходимые поля также обрабатываются
        )
        db.add(db_employee)
        db.commit()
        db.refresh(db_employee)
        return db_employee
    except Exception as e:
        logger.error(f"Ошибка создания сотрудника: {e}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


# Эндпоинт для получения данных о сотруднике, связанном с текущим аутентифицированным пользователем
@router.get("/user-employee/", response_model=EmployeeResponse)
def read_user_employee(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.id == current_user.employee_id).first()
    if employee is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Сотрудник не найден")
    return employee

# Эндпоинт для получения списка сотрудников
@router.get("/", response_model=List[EmployeeResponse])
def get_employees(db: Session = Depends(get_db)):
    employees = db.query(Employee).all()
    if not employees:
        raise HTTPException(status_code=404, detail="Сотрудники не найдены")
    return employees

# Эндпоинт для получения информации о сотруднике по ID
@router.get("/{employee_id}", response_model=EmployeeResponse)
def get_employee_by_id(employee_id: int, db: Session = Depends(get_db)):
    logger.info(f"Получение информации о сотруднике с ID={employee_id}")
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if employee is None:
        logger.error(f"Сотрудник с ID={employee_id} не найден")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Сотрудник не найден")
    logger.info(f"Информация о сотруднике с ID={employee_id} успешно получена")
    return employee

# Эндпоинт для обновления данных сотрудника
@router.put("/{employee_id}")
async def update_employee(
    employee_id: int,
    FIO: str = Form(...),
    surname: str = Form(...),
    post: str = Form(...),
    email: str = Form(...),
    phone: str = Form(...),
    photo: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    try:
        db_employee = db.query(Employee).filter(Employee.id == employee_id).first()
        if db_employee:
            db_employee.FIO = FIO
            db_employee.surname = surname
            db_employee.post = post
            db_employee.email = email
            db_employee.phone = phone

            if photo:
                photo_content = await photo.read()
                db_employee.photo = photo_content

            db.commit()
            db.refresh(db_employee)
            return {"message": "Employee updated successfully!"}
        else:
            raise HTTPException(status_code=404, detail="Employee not found")
    except Exception as e:
        logger.error(f"Ошибка при обновлении сотрудника {employee_id}: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# Эндпоинт для удаления сотрудника
@router.delete("/{employee_id}")
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    logger.info(f"Удаление сотрудника с ID={employee_id}")
    
    db_employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not db_employee:
        logger.error(f"Сотрудник с ID={employee_id} не найден")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Сотрудник не найден")

    try:
        db.query(User).filter(User.employee_id == employee_id).delete(synchronize_session=False)
        db.delete(db_employee)
        db.commit()
        logger.info(f"Сотрудник с ID={employee_id} успешно удален")
        return {"message": "Сотрудник успешно удален"}
    except Exception as e:
        logger.error(f"Ошибка при удалении сотрудника с ID={employee_id}: {e}")
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ошибка при удалении сотрудника")

# Эндпоинт для загрузки фотографии сотрудника
@router.put("/{employee_id}/upload-photo/")
async def upload_photo(
    employee_id: int,
    photo: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    logger.info(f"Загрузка фото для сотрудника с ID={employee_id}")
    db_employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not db_employee:
        logger.error(f"Сотрудник с ID={employee_id} не найден")
        raise HTTPException(status_code=404, detail="Сотрудник не найден")

    photo_content = await photo.read()
    logger.info(f"Фото загружено. Размер: {len(photo_content)} байт")

    db_employee.photo = photo_content
    db.commit()
    db.refresh(db_employee)

    logger.info(f"Фото для сотрудника с ID={employee_id} успешно сохранено")
    return {"message": "Фото успешно загружено!"}

# Эндпоинт для получения фотографии сотрудника
@router.get("/{employee_id}/photo/")
def get_photo(employee_id: int, db: Session = Depends(get_db)):
    logger.info(f"Получение фото для сотрудника с ID={employee_id}")
    db_employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not db_employee or not db_employee.photo:
        logger.error(f"Фото для сотрудника с ID={employee_id} не найдено")
        raise HTTPException(status_code=404, detail="Фото сотрудника не найдено")

    logger.info(f"Фото для сотрудника с ID={employee_id} успешно получено")
    return StreamingResponse(io.BytesIO(db_employee.photo), media_type="image/jpeg")
