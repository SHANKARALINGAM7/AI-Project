from typing import Dict, List, Optional, TypedDict
from datetime import date
from pydantic import BaseModel
  
class ProductDetails(TypedDict):
    product_name : str
    category : str
    current_quantity : int
    threshold_quantity : int
    min_order_quantity : int
    
class SupplierDetails(TypedDict):
    supplier_name : str
    lead_time_days : int
    min_order_value : int
    
class ProductWithQuantity(TypedDict):
    product_id:int
    order_quantity:int
    
class FestivalDemand(BaseModel):
    festival_name: str
    date: date
    demand_categories: List[str]
    demand_level: str  #(Low | Medium | High)
    
class FestivalDemandOutput(BaseModel):
    festivals: List[FestivalDemand]
    
class FestivalImpactByCategory(TypedDict):
    festival_name: str
    date: str
    demand_level: str
    
class OrderDraftResponse(BaseModel):
    order_number: str
    supplier_id: int
    supplier_name: Optional[str]
    product_id: int
    product_name: str
    category: str
    current_quantity: int
    suggested_quantity: int
    festival_name: Optional[str]
    festival_impact_level: Optional[str]

class AgentState(TypedDict):
    products: Dict[int, ProductDetails]             # product_id → product info
    suppliers : Dict[int,SupplierDetails]           # supplier_id -> supplier info
    prophet_prediction: Dict[int, int]              # product_id → predicted qty
    finalized_order_quantity: Dict[int, int]        # product_id → final qty
    supplier_map_with_product: Dict[int, ProductWithQuantity]
    
    festival_impacts: Dict[str,List[FestivalImpactByCategory]]         
    weather_impacts: List[str]
    
    response : List[OrderDraftResponse]
