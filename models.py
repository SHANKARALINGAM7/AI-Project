from sqlalchemy import Column, Integer, String, Text, Date, Numeric, ForeignKey
from core.database import Base

class Supplier(Base):
    __tablename__ = "supplier"

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    contact_email = Column(Text)
    lead_time_days = Column(Integer, default=3)
    min_order_value = Column(Numeric(10, 2), default=0.00)


class Product(Base):
    __tablename__ = "products"

    product_id = Column(Integer, primary_key=True)
    sku = Column(String(50), unique=True, nullable=False)
    name = Column(Text, nullable=False)
    category = Column(String(20))
    current_quantity = Column(Integer, nullable=False)
    threshold_quantity = Column(Integer, nullable=False)
    unit_price = Column(Numeric(10, 2), nullable=False)
    min_order_qty = Column(Integer, default=1)


class ProductSupplier(Base):
    __tablename__ = "product_suppliers"

    id = Column(Integer, primary_key=True)
    supplier_id = Column(Integer, ForeignKey("supplier.id", ondelete="CASCADE"))
    product_id = Column(Integer, ForeignKey("products.product_id", ondelete="CASCADE"))
    supplier_price = Column(Numeric(10, 2))
    supplier_sku = Column(String(50))


class SalesHistory(Base):
    __tablename__ = "sales_history"

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("products.product_id", ondelete="CASCADE"))
    sale_date = Column(Date, nullable=False)
    quantity_sold = Column(Integer, nullable=False)


class POItem(Base):
    __tablename__ = "po_items"

    id = Column(Integer, primary_key=True)
    po_id = Column(Integer)
    product_id = Column(Integer, ForeignKey("products.product_id"))
    prophet_forecast = Column(Integer)
    ai_suggested_qty = Column(Integer)
    ai_reasoning = Column(Text)
    

class FestivalMaster(Base):
    __tablename__ = 'festival_master'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    festival_date = Column(Date, nullable=False, index=True)
    festival_name = Column(String(255), nullable=False)
    description = Column(Text)
