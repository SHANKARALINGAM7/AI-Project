from langgraph.graph import START,END,StateGraph
from state import AgentState
from nodes import (
    init_state,
    quantity_finalizer,
    quantity_predictor,
    product_mapper,
    festival_demand_analyzer,
    weather_demand_analyzer,
    response_formatter)



def build_graph():
    
    graph = StateGraph(AgentState)
    
    #Nodes 
    graph.add_node("Initializer",init_state)
    graph.add_node("Prophet Prediction",quantity_predictor)
    graph.add_node("Quantity Finalizer",quantity_finalizer)
    graph.add_node("Product Mapper",product_mapper)
    graph.add_node("Festival Analyzer",festival_demand_analyzer)
    graph.add_node("Weather Analyzer",weather_demand_analyzer)
    graph.add_node("Response Formatter",response_formatter)
    
    #Edges
    graph.add_edge(START,"Initializer")
    graph.add_edge("Initializer","Prophet Prediction")
    graph.add_edge("Prophet Prediction","Quantity Finalizer")
    graph.add_edge("Quantity Finalizer","Product Mapper")
    graph.add_edge("Product Mapper","Festival Analyzer")
    graph.add_edge("Festival Analyzer","Weather Analyzer")
    graph.add_edge("Weather Analyzer","Response Formatter")
    graph.add_edge("Response Formatter",END)
    
    return graph.compile()

final_graph = build_graph()