from models import FestivalMaster, Product, ProductSupplier, SalesHistory, Supplier
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date, timedelta

def get_sales_bulk(db: Session,days: int = 150):
    """
    Fetch sales history for given products and aggregate quantity sold per day
    """
    start_date = date.today() - timedelta(days=days)

    # Aggregate quantity_sold per product_id per day
    rows = (
        db.query(
            SalesHistory.product_id,
            SalesHistory.sale_date,
            func.sum(SalesHistory.quantity_sold).label("quantity_sold")
        ).join(Product,Product.product_id == SalesHistory.product_id)
        .filter(
            SalesHistory.sale_date >= start_date,
            Product.current_quantity <= Product.threshold_quantity
            
        )
        .group_by(SalesHistory.product_id, SalesHistory.sale_date)
        .order_by(SalesHistory.product_id, SalesHistory.sale_date)
        .all()
    )

    return rows


def get_supplier_products(db:Session):
    
    data = db.query(ProductSupplier
                    ).order_by(ProductSupplier.product_id).all()
    return data

def get_all_suppliers(db:Session):
    
    data = db.query(Supplier).all()
    return data


def get_products(db:Session):
    
    products = db.query(Product
                        ).filter(Product.current_quantity <= Product.threshold_quantity).all()
    return products


def get_festivals(db:Session,start,end):
    
    
    start_date = date.today() + timedelta(days=start)
    end_date = date.today() + timedelta(days=end)
    festivals = db.query(FestivalMaster
                         ).filter(FestivalMaster.festival_date >= start_date,
                                  FestivalMaster.festival_date <= end_date)
                         
    return festivals