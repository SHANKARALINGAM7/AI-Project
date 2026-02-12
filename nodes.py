from agents.festival_analyzer import analyze_festival_demand
from utils.festival_mapper import festival_list_to_category_map
from utils.finalize_quantity import finalize_order_quantity
from utils.helper import product_list_to_dict, supplier_list_to_dict
from utils.mapper import product_supplier_mapper
from agents.predictor import get_prediction
from agents.weather_analyzer import analyze_weather_demand
from crud import get_all_suppliers, get_products
from state import AgentState
from core.database import session
from sqlalchemy.orm import Session
from utils.structure_output import convert_to_json


def init_state(state:AgentState)-> AgentState:
    db: Session = session()
    products = get_products(db)
    suppliers = get_all_suppliers(db)
    product_map = product_list_to_dict(products)
    supplier_map = supplier_list_to_dict(suppliers)

    db.close()  
    return {
        "products": product_map,
        "suppliers":supplier_map,
        "prophet_prediction": {},
        "finalized_order_quantity": {},
        "supplier_map_with_product": {},
        "festival_impacts": {},
        "weather_impacts": [],
        "response":[]
     }
    

def quantity_predictor(state:AgentState)-> AgentState:
    
    db:Session = session()
    prophet_prediction = get_prediction(db,forecast_days=30)
    db.close()
    
    print("================================================================")
    print(f"prophet prediction :{prophet_prediction}")
    return {
        **state,
        "prophet_prediction":prophet_prediction
    }
    
    
def quantity_finalizer(state:AgentState)-> AgentState:
    
    """finalize the needed quantity using prophet prediction """
    products = state["products"]
    prophet_prediction = state["prophet_prediction"]
    
    finalize_quantity = finalize_order_quantity(products,prophet_prediction)
    
    print("================================================================")
    print(f"finalized quantity :{finalize_quantity}")
    
    return {
        **state,
        "finalized_order_quantity":finalize_quantity
    }    


def product_mapper(state:AgentState)->AgentState:
    
    finalize_quantity = state["finalized_order_quantity"]
    db:Session = session()
    final_grouping = product_supplier_mapper(db,finalize_quantity,state["suppliers"])
    db.close()
  
    return {
        **state,
        "supplier_map_with_product":final_grouping
    }
    
    
def festival_demand_analyzer(state: AgentState) -> AgentState:
    
    products = state["products"]
    festival_impacts = analyze_festival_demand(products)
    
    category_festival_map = festival_list_to_category_map(festival_impacts)
    
    print(category_festival_map)
    return {
        **state,
        "festival_impacts": category_festival_map
    }
    
    
def weather_demand_analyzer(state:AgentState)->AgentState:
    

    weather_impacts = analyze_weather_demand()
    
    return {
        **state,
        "weather_impacts":weather_impacts
    }


def response_formatter(state:AgentState):
    response = convert_to_json(state)
    
    return {
        **state,
        "response":response
    } 