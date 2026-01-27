def product_list_to_dict(products):
    product_map = {}
    
    for p in products:
        product_map[p.product_id] = {
                    "product_name": p.name,
                    "category": p.category,
                    "current_quantity": p.current_quantity,
                    "threshold_quantity": p.threshold_quantity,
                    "min_order_quantity": p.min_order_qty,
        }
    return product_map
    
def supplier_list_to_dict(suppliers):
    supplier_map = {}
    
    for s in suppliers:
        supplier_map[s.id] = {
                    "supplier_name": s.name,
                    "lead_time_days": s.lead_time_days,
                    "min_order_value": s.min_order_value,
        }
    return supplier_map