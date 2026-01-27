from sqlalchemy.orm import Session
from crud import get_supplier_products

def product_supplier_mapper(db:Session,finalize_quantity,suppliers):
    """
       Supplier selection strategy:Choose supplier with minimum lead time
       Assumes faster delivery reduces stockout risk
    """

    supplier_with_products = get_supplier_products(db)
    
    ## in the of form product id : List[supplier id]
    product_map = {}
    
    for p in supplier_with_products:
        if p.product_id in product_map:
           product_map[p.product_id].append(p.supplier_id)
        else:
            product_map[p.product_id] = [p.supplier_id]
            
            
    supplier_map = {}
    for s_id,data in suppliers.items():
        supplier_map[s_id] = {
                    "name": suppliers[s_id]["supplier_name"],
                    "lead_time": suppliers[s_id]["lead_time_days"],
                    "min_order_value": suppliers[s_id]["min_order_value"]
                }

        
        
    ## in the form of key supplier id :[[product_id,needed quantity]]
    final_grouping = {}
    
    print(finalize_quantity)
    for product_id,quantity in finalize_quantity.items():
        
        if product_id not in product_map:
            continue
        
        suppliers_of_product_id = product_map[product_id]
        min_lead_time = float("inf")
        selected_supplier_id = None
        
        for s_id in suppliers_of_product_id:
            if supplier_map[s_id]["lead_time"] < min_lead_time:
                min_lead_time = supplier_map[s_id]["lead_time"]
                selected_supplier_id = s_id
                
        if selected_supplier_id is not None:
            if selected_supplier_id in final_grouping:
                final_grouping[selected_supplier_id].append([product_id,quantity])
            
            else:
                final_grouping[selected_supplier_id] = [[product_id,quantity]]
                
    return final_grouping
      