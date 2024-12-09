from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, LargeBinary
from sqlalchemy.orm import relationship
from base_class import Base  # Убедитесь, что импортируете Base из database
from passlib.hash import sha256_crypt

class Employee(Base):
    __tablename__ = 'employee'
    id = Column(Integer, primary_key=True, index=True)
    FIO = Column(String, index=True, nullable=False)
    surname = Column(String, index=True, nullable=False)
    company_id = Column(Integer, ForeignKey('company.id'), nullable=True)
    post = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=True)
    phone = Column(String, unique=True, index=True, nullable=True)
    photo = Column(LargeBinary, nullable=True)

    company = relationship("Company", back_populates="employees")
    cart_items = relationship("Cart", back_populates="employee")  
class Company(Base):
    __tablename__ = 'company'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    warehouse = Column(String)
    inn = Column(String, unique=True, index=True)
    employees = relationship("Employee", back_populates="company")
    warehouses = relationship("Warehouse", back_populates="company")

class Warehouse(Base):
    __tablename__ = 'warehouse'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    company_id = Column(Integer, ForeignKey('company.id'))
    products = relationship("Product", back_populates="warehouse")
    company = relationship("Company", back_populates="warehouses")

class Product(Base):
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    manufacturer = Column(String, index=True)
    article_p = Column(String)
    article_v = Column(String)
    cost = Column(Float)
    factory_number = Column(Integer, unique=True, index=True)
    account_id = Column(Integer, ForeignKey('account.id'))
    upd_id = Column(Integer, ForeignKey('upd.id'))
    supplier_id = Column(Integer, ForeignKey('supplier.id'))
    category_id = Column(Integer, ForeignKey('category_prod.id'))
    storage_location_id = Column(Integer, ForeignKey('storage_location.id'))
    warehouse_id = Column(Integer, ForeignKey('warehouse.id'))
    employee_id = Column(Integer, ForeignKey('employee.id'))
    photo = Column(LargeBinary)
    quantity = Column(Integer, default=1)  # New field to track quantity

    warehouse = relationship("Warehouse", back_populates="products")
    supplier = relationship("Supplier")
    category = relationship("Category_prod")
    storage_location = relationship("Storage_location")
    employee = relationship("Employee")
    account = relationship("Account")
    upd = relationship("UPD")

class Category_prod(Base):
    __tablename__ = 'category_prod'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    company_id = Column(Integer, ForeignKey('company.id'))
    products = relationship("Product", back_populates="category")

class Supplier(Base):
    __tablename__ = 'supplier'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    inn = Column(String, unique=True, index=True)
    ur_adress = Column(String)
    payment_account = Column(String)
    bank = Column(String)
    bik = Column(String)
    corr_account = Column(String)
    fio_manager = Column(String)
    email = Column(String, unique=True, index=True)
    phone = Column(String, unique=True, index=True)
    products = relationship("Product", back_populates="supplier")
    accounts = relationship("Account", back_populates="supplier")

class Account(Base):
    __tablename__ = 'account'
    id = Column(Integer, primary_key=True, index=True)
    account_number = Column(Integer)
    account_pdf = Column(LargeBinary, nullable=False)
    supplier_id = Column(Integer, ForeignKey('supplier.id'))
    summ = Column(Float)
    supplier = relationship("Supplier", back_populates="accounts")

class UPD(Base):
    __tablename__ = 'upd'
    id = Column(Integer, primary_key=True, index=True)
    doc_number = Column(Integer, unique=True, index=True)
    supplier_id = Column(Integer, ForeignKey('supplier.id'))
    upd_pdf = Column(LargeBinary, nullable=False)

class Storage_location(Base):
    __tablename__ = 'storage_location'
    id = Column(Integer, primary_key=True, index=True)
    shelving_number = Column(Integer, nullable=False)
    shelf_number = Column(Integer, nullable=False)
    description = Column(String, nullable=True)
    location_count = Column(Integer, default=0)  # New field to track location count
    products = relationship("Product", back_populates="storage_location")

# In models.py

class Cart(Base):
    __tablename__ = 'cart'
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey('employee.id'), nullable=False)  # Связываем с Employee
    product_id = Column(Integer, ForeignKey('product.id'), nullable=False)
    quantity = Column(Integer, default=1)

    employee = relationship("Employee", back_populates="cart_items")  # Новая связь с Employee
    product = relationship("Product")


# Update the User model to include a relationship with the Cart
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    email = Column(String, unique=True, index=True, nullable=True)
    is_active = Column(Boolean, default=True)
    employee_id = Column(Integer, ForeignKey('employee.id'))
    
    def verify_password(self, password: str):
        return sha256_crypt.verify(password, self.hashed_password)
