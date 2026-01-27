from graph import final_graph

result = final_graph.invoke({})
products = result["products"]
print("===================================================================")
# print(products)
print("Result :")

for s_id, data in result["supplier_map_with_product"].items():
    print(f"Supplier : id {s_id} :")
    for d in data:
        p_id = d[0]
        quantity = d[1]
        product = products[p_id]
        print(f"{product['product_name']} - Quantity : {quantity}")
    print("===================================================================")
    
