from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from typing import List
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Product, Supplier, Category_prod, Storage_location, Warehouse, Employee, UPD, Account  # Import UPD and Account
from pydantic import BaseModel
import logging
import io
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import joinedload
from typing import Optional

router = APIRouter()

logger = logging.getLogger(__name__)


# Pydantic модели для работы с продуктами и связанными сущностями
class ProductBase(BaseModel):
    name: str
    manufacturer: str
    article_p: str
    article_v: str
    cost: float
    factory_number: int
    account_id:int
    upd_id:int
    supplier_id: int
    category_id: int
    storage_location_id: int
    warehouse_id: int
    employee_id: int
    quantity: int = 1  # New field for quantity

class StorageLocationResponse(BaseModel):
    id: int
    shelving_number: int
    shelf_number: int
    description: str
    location_count: int  # Include the new location count field

    class Config:
        from_attributes = True  # Используется для автоматической конфигурации из атрибутов ORM
        
class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: int
    storage_location: StorageLocationResponse  # Вложенная модель для хранения данных о стеллаже и полке
    
    class Config:
        from_attributes = True


class SupplierResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

class CategoryResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

class StorageLocationResponse(BaseModel):
    id: int
    shelving_number: int
    shelf_number: int
    description: str
    location_count: int

    class Config:
        from_attributes = True

class WarehouseResponse(BaseModel):
    id: int
    name: str
    company_id: int

    class Config:
        from_attributes = True

class UPDResponse(BaseModel):
    id: int
    doc_number: int
    supplier_id: int

    class Config:
        from_attributes = True

class AccountResponse(BaseModel):
    id: int
    account_number: int
    supplier_id: int
    summ: float

    class Config:
       from_attributes = True

class SupplierResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

class CategoryResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

class WarehouseResponse(BaseModel):
    id: int
    name: str
    company_id: int

    class Config:
        from_attributes = True

# Функция для получения сессии базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/storage-locations/", response_model=StorageLocationResponse)
def create_storage_location(
    shelving_number: int = Form(...),
    shelf_number: int = Form(...),
    description: str = Form(...),
    location_count: int = Form(...),  # New field for number of locations
    db: Session = Depends(get_db)
):
    try:
        storage_location = Storage_location(
            shelving_number=shelving_number,
            shelf_number=shelf_number,
            description=description,
            location_count=location_count  # Set the count when creating the storage location
        )
        db.add(storage_location)
        db.commit()
        db.refresh(storage_location)
        return storage_location
    except Exception as e:
        # Check for uniqueness constraint error
        if 'unique_shelving_shelf' in str(e):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Местоположение с таким стеллажом и полкой уже существует.")
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Внутренняя ошибка сервера: {e}")


@router.post("/", response_model=ProductResponse)
async def create_product(
    name: str = Form(...),
    manufacturer: str = Form(...),
    article_p: str = Form(...),
    article_v: str = Form(...),
    cost: float = Form(...),
    factory_number: int = Form(...),
    account_id: int = Form(...),
    upd_id: int = Form(...),
    supplier_id: int = Form(...),
    category_id: int = Form(...),
    storage_location_id: int = Form(...),
    warehouse_id: int = Form(...),
    employee_id: int = Form(...),
    quantity: int = Form(...),  # New field for product quantity
    photo: UploadFile = File(None),  # Optional photo upload
    db: Session = Depends(get_db)
):
    logger.info(f"Создание продукта: {name}")

    # Validate related entities
    if not db.query(Supplier).filter(Supplier.id == supplier_id).first():
        logger.error(f"Поставщик с ID={supplier_id} не найден")
        raise HTTPException(status_code=404, detail="Поставщик не найден")
    if not db.query(Category_prod).filter(Category_prod.id == category_id).first():
        logger.error(f"Категория с ID={category_id} не найдена")
        raise HTTPException(status_code=404, detail="Категория не найдена")
    if not db.query(Storage_location).filter(Storage_location.id == storage_location_id).first():
        logger.error(f"Место хранения с ID={storage_location_id} не найдено")
        raise HTTPException(status_code=404, detail="Место хранения не найдено")
    if not db.query(Warehouse).filter(Warehouse.id == warehouse_id).first():
        logger.error(f"Склад с ID={warehouse_id} не найден")
        raise HTTPException(status_code=404, detail="Склад не найден")
    if not db.query(Employee).filter(Employee.id == employee_id).first():
        logger.error(f"Сотрудник с ID={employee_id} не найден")
        raise HTTPException(status_code=404, detail="Сотрудник не найден")

    # Read and store photo if provided
    photo_data = None
    if photo:
        photo_data = await photo.read()
        logger.info(f"Фото продукта загружено, размер: {len(photo_data)} байт")

    # Create the product instance
    db_product = Product(
        name=name,
        manufacturer=manufacturer,
        article_p=article_p,
        article_v=article_v,
        cost=cost,
        factory_number=factory_number,
        account_id=account_id,
        upd_id=upd_id,
        supplier_id=supplier_id,
        category_id=category_id,
        storage_location_id=storage_location_id,
        warehouse_id=warehouse_id,
        employee_id=employee_id,
        quantity=quantity,  # Set the quantity for the product
        photo=photo_data  # Save photo data
    )

    db.add(db_product)

    # Update the location count
    storage_location = db.query(Storage_location).filter(Storage_location.id == storage_location_id).first()
    if storage_location:
        storage_location.location_count += quantity

    db.commit()
    db.refresh(db_product)
    logger.info(f"Продукт создан: {db_product}")

    return db_product

@router.get("/products/{product_id}/photo")
def get_product_photo(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product or not product.photo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Фот  о не найдено")
    
    return StreamingResponse(io.BytesIO(product.photo), media_type="image/jpeg")

@router.get("/", response_model=List[ProductResponse])
def read_products(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    products = db.query(Product).options(joinedload(Product.storage_location)).offset(skip).limit(limit).all()
    return products


@router.get("/{product_id}", response_model=ProductResponse)
def read_product_by_id(product_id: int, db: Session = Depends(get_db)):
    logger.info(f"Fetching product with id={product_id}")
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        logger.error(f"Product with id={product_id} not found")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    logger.info(f"Product fetched: {product}")
    return product

# Эндпоинт для получения списка поставщиков
@router.get("/suppliers/", response_model=List[SupplierResponse])
def read_suppliers(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    suppliers = db.query(Supplier).offset(skip).limit(limit).all()
    return suppliers

# Эндпоинт для получения списка категорий
@router.get("/categories/", response_model=List[CategoryResponse])
def read_categories(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    categories = db.query(Category_prod).offset(skip).limit(limit).all()
    return categories

# Эндпоинт для получения списка мест хранения
@router.get("/storage-locations/", response_model=List[StorageLocationResponse])
def read_storage_locations(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    storage_locations = db.query(Storage_location).offset(skip).limit(limit).all()
    return storage_locations

# Эндпоинт для получения списка складов
@router.get("/warehouses/", response_model=List[WarehouseResponse])
def read_warehouses(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    warehouses = db.query(Warehouse).offset(skip).limit(limit).all()
    return warehouses

# CRUD функции для UPD и счетов
def create_upd(db: Session, doc_number: int, supplier_id: int, upd_pdf: bytes) -> Product:
    db_upd = UPD(doc_number=doc_number, supplier_id=supplier_id, upd_pdf=upd_pdf)
    db.add(db_upd)
    db.commit()
    db.refresh(db_upd)
    return db_upd

def get_upd_by_id(db: Session, upd_id: int) -> Product:
    return db.query(UPD).filter(UPD.id == upd_id).first()

# Эндпоинты для работы с UPD
@router.post("/upds/", response_model=UPDResponse)
async def create_upd_endpoint(
    doc_number: int = Form(...),
    supplier_id: int = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    logger.info(f"Создание UPD с номером документа={doc_number}")
    
    try:
        upd_content = await file.read()
        logger.info(f"Файл загружен. Размер: {len(upd_content)} байт")
        
        supplier = db.query(Supplier).filter(Supplier.id == supplier_id).first()
        if not supplier:
            logger.warning(f"Поставщик с ID {supplier_id} не найден")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Поставщик не найден")
        
        db_upd = create_upd(db, doc_number, supplier_id, upd_content)
        
        logger.info(f"UPD с номером документа={doc_number} успешно создан")
        return db_upd
    except Exception as e:
        logger.error(f"Ошибка при создании UPD с номером документа={doc_number}: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Внутренняя ошибка сервера: {e}")

@router.get("/upds/{upd_id}/pdf")
def get_upd_pdf(upd_id: int, db: Session = Depends(get_db)):
    upd = get_upd_by_id(db, upd_id)
    if not upd:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="UPD не найден")
    
    pdf_content = upd.upd_pdf
    return StreamingResponse(io.BytesIO(pdf_content), media_type="application/pdf")

# Эндпоинты для работы со счетами
@router.post("/invoices/", response_model=AccountResponse)
async def create_invoice(
    account_number: int = Form(...),
    supplier_id: int = Form(...),
    summ: float = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    logger.info(f"Создание счета-фактуры с номером={account_number}")

    try:
        pdf_content = await file.read()
        logger.info(f"Файл загружен. Размер: {len(pdf_content)} байт")

        supplier = db.query(Supplier).filter(Supplier.id == supplier_id).first()
        if not supplier:
            logger.warning(f"Поставщик с ID {supplier_id} не найден")
            raise HTTPException(status_code=404, detail="Поставщик не найден")

        db_invoice = Account(
            account_number=account_number,
            account_pdf=pdf_content,
            supplier_id=supplier_id,
            summ=summ
        )

        db.add(db_invoice)
        db.commit()
        db.refresh(db_invoice)

        logger.info(f"Счет-фактура с номером={account_number} успешно создан")
        return {
            "account_number": db_invoice.account_number,
            "supplier_id": db_invoice.supplier_id,
            "summ": db_invoice.summ,
            "id": db_invoice.id  # Возвращаем ID счета
        }
    except Exception as e:
        logger.error(f"Ошибка при создании счета-фактуры с номером={account_number}: {e}")
        raise HTTPException(status_code=500, detail=f"Внутренняя ошибка сервера: {e}")

@router.get("/invoices/{invoice_id}/pdf")
def get_invoice_pdf(invoice_id: int, db: Session = Depends(get_db)):
    invoice = db.query(Account).filter(Account.id == invoice_id).first()
    if not invoice:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Счет-фактура не найдена")

    pdf_content = invoice.account_pdf
    return StreamingResponse(io.BytesIO(pdf_content), media_type="application/pdf")

# Эндпоинт для поиска продуктов по идентификатору сотрудника
@router.get("/employee/{employee_id}", response_model=List[ProductResponse])
def get_products_by_employee(employee_id: int, db: Session = Depends(get_db)):
    logger.info(f"Поиск продуктов по сотруднику с ID={employee_id}")
    products = db.query(Product).filter(Product.employee_id == employee_id).all()
    if not products:
        logger.warning(f"Продукты для сотрудника с ID={employee_id} не найдены")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Продукты не найдены")
    logger.info(f"Найдено {len(products)} продуктов для сотрудника с ID={employee_id}")
    return products

@router.put("/transfer-products/")
def transfer_products(
    from_employee_id: int = Form(...),
    to_employee_id: int = Form(...),
    db: Session = Depends(get_db)
):
    logger.info(f"Перенос продуктов от сотрудника {from_employee_id} к сотруднику {to_employee_id}")

    products = db.query(Product).filter(Product.employee_id == from_employee_id).all()

    if not products:
        logger.warning(f"Продукты, связанные с сотрудником {from_employee_id}, не найдены")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Продукты не найдены")

    try:
        for product in products:
            product.employee_id = to_employee_id
            db.commit()
            db.refresh(product)

        logger.info(f"Продукты успешно переданы от сотрудника {from_employee_id} к сотруднику {to_employee_id}")
        return {"message": f"Продукты успешно переданы сотруднику {to_employee_id}"}

    except Exception as e:
        logger.error(f"Ошибка при переносе продуктов от сотрудника {from_employee_id} к сотруднику {to_employee_id}: {e}")
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ошибка при переносе продуктов")

@router.put("/transfer-product/")
def transfer_product(
    product_id: int = Form(...),
    from_employee_id: int = Form(...),
    to_employee_id: int = Form(...),
    db: Session = Depends(get_db)
):
    logger.info(f"Перенос продукта {product_id} от сотрудника {from_employee_id} к сотруднику {to_employee_id}")

    product = db.query(Product).filter(Product.id == product_id, Product.employee_id == from_employee_id).first()

    if not product:
        logger.warning(f"Продукт с ID {product_id}, принадлежащий сотруднику {from_employee_id}, не найден")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Продукт не найден или не принадлежит указанному сотруднику")

    try:
        product.employee_id = to_employee_id
        db.commit()
        db.refresh(product)

        logger.info(f"Продукт {product_id} успешно передан от сотрудника {from_employee_id} к сотруднику {to_employee_id}")
        return {"message": f"Продукт {product_id} успешно передан сотруднику {to_employee_id}"}

    except Exception as e:
        logger.error(f"Ошибка при переносе продукта {product_id} от сотрудника {from_employee_id} к сотруднику {to_employee_id}: {e}")
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ошибка при переносе продукта")
@router.post("/suppliers/", response_model=SupplierResponse)
def create_supplier(
    name: str = Form(...),
    inn: str = Form(...),
    ur_adress: str = Form(...),
    payment_account: str = Form(...),
    bank: str = Form(...),
    bik: str = Form(...),
    corr_account: str = Form(...),
    fio_manager: str = Form(...),
    email: str = Form(...),
    phone: str = Form(...),
    db: Session = Depends(get_db)
):
    try:
        supplier = Supplier(
            name=name,
            inn=inn,
            ur_adress=ur_adress,
            payment_account=payment_account,
            bank=bank,
            bik=bik,
            corr_account=corr_account,
            fio_manager=fio_manager,
            email=email,
            phone=phone
        )
        db.add(supplier)
        db.commit()
        db.refresh(supplier)
        return supplier
    except Exception as e:
        if 'unique' in str(e):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Поставщик с таким ИНН или email уже существует.")
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Внутренняя ошибка сервера: {e}")
@router.post("/categories/", response_model=CategoryResponse)
def create_category(
    name: str = Form(...),
    company_id: int = Form(...),
    db: Session = Depends(get_db)
):
    try:
        category = Category_prod(
            name=name,
            company_id=company_id
        )
        db.add(category)
        db.commit()
        db.refresh(category)
        return category
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Внутренняя ошибка сервера: {e}")
@router.post("/warehouses/", response_model=WarehouseResponse)
def create_warehouse(
    name: str = Form(...),
    company_id: int = Form(...),
    db: Session = Depends(get_db)
):
    try:
        warehouse = Warehouse(
            name=name,
            company_id=company_id
        )
        db.add(warehouse)
        db.commit()
        db.refresh(warehouse)
        return warehouse
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Внутренняя ошибка сервера: {e}")
@router.get("/cart", response_model=List[ProductResponse])
def get_cart_items(db: Session = Depends(get_db)):
    """
    Возвращает все товары в корзине.
    """
    # Предположим, что у вас есть поле, которое определяет, находится ли товар в корзине.
    products_in_cart = db.query(Product).filter(Product.is_in_cart == True).all()
    if not products_in_cart:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Корзина пуста")
    return products_in_cart

