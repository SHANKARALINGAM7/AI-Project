def finalize_order_quantity(products,prophet_prediction):
     
    finalize_quantity = {}
    
    for product_id,data in products.items():
        
        
        if product_id not in prophet_prediction:
            finalize_quantity[product_id] = int(data["threshold_quantity"]/10 * 30) + data["min_order_quantity"]
            continue
        ## needed quantity calculated by sum of (quantity predicted by prophet + threshold quantity) - currrent-quantity
        
        needed_quantity = prophet_prediction[product_id] + data["threshold_quantity"] - data["current_quantity"]
        ## each product have the min order quantity if the predicted quantity below the that then 
        ## needed quantity changed to min order quantity
        needed_quantity = max(needed_quantity,data["min_order_quantity"])
        
        finalize_quantity[product_id] = needed_quantity
        
    return finalize_quantity
        