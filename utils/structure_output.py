import uuid
from typing import List
from state import AgentState


def convert_to_json(state: AgentState) -> List[dict]:

    products = state["products"]
    supplier_map = state["supplier_map_with_product"]
    festival_impacts = state["festival_impacts"]
    response = []
    suppliers = state["suppliers"]
    order_number = f"PO-{uuid.uuid4().hex[:8].upper()}"

    for supplier_id, items in supplier_map.items():
        for product_id, suggested_qty in items:

            product = products[product_id]
            category = product["category"]

            # Default festival values
            festival_name = None
            festival_level = None

            # Attach first relevant festival (nearest / strongest)
            if category in festival_impacts and festival_impacts[category]:
                fest = festival_impacts[category][0]
                festival_name = fest["festival"]
                festival_level = fest["demand_level"]

            response.append({
                "order_number": order_number+""+str(supplier_id),
                "supplier_id": supplier_id,
                "supplier_name": suppliers[supplier_id]["supplier_name"],  
                "product_id": product_id,   
                "product_name": product["product_name"],
                "category": category,
                "current_quantity": product["current_quantity"],
                "suggested_quantity": suggested_qty,
                "festival_name": festival_name,
                "festival_impact_level": festival_level
            })

    return response
