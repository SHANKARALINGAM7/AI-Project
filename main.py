from fastapi import FastAPI
from core.database import engine
import models
from graph import final_graph
from state import OrderDraftResponse
from fastapi.middleware.cors import CORSMiddleware
# https://reachcoimbatore.com/upcoming-festivals

app = FastAPI(title="PO Automation API")

models.Base.metadata.create_all(bind=engine)
origins = [
    "http://127.0.0.1:5500",
    "http://localhost:5500",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/generate-po", response_model=list[OrderDraftResponse])
def generate_purchase_order():
    
    result = final_graph.invoke({})
    return result["response"]