from core.database import session
from sqlalchemy.orm import Session
from crud import get_festivals
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from state import FestivalDemand, FestivalDemandOutput

load_dotenv()

def fetch_festival_data():
    
     db:Session = session()
     start_date_from_today = 0
     end_date_from_start = 30
     festivals = get_festivals(db,start_date_from_today,end_date_from_start)
     db.close()
     
     
     festivals_data = [
               {
                   "date": f.festival_date,
                   "festival_name": f.festival_name,
                   "description": f.description
               }
           for f in festivals]
     
     return festivals_data
     
     
def analyze_festival_demand(products):
    """
    Uses LLM to analyze which product categories may see increased demand
    during upcoming festivals 
    """
    
    llm = ChatGroq(
        # model="llama-3.1-8b-instant",
        model="qwen/qwen3-32b",
        temperature=0
    ).with_structured_output(FestivalDemandOutput)

    categories = set()
    for id,product in products.items():
        categories.add(products[id]["category"])
    festivals = fetch_festival_data()

    
    system_prompt = """
                     You are an Inventory Purchase Order Assistant.
                     
                     RULES (VERY IMPORTANT):
                     - Use ONLY the festivals provided.
                     - Use ONLY the product categories provided.
                     - Do NOT invent festivals, dates, or categories.
                     - If a festival has no impact, return an empty list.
                     - Always return valid JSON matching the schema.
                   """

    human_prompt = f"""Upcoming festivals:{festivals}  
                       Available product categories:{categories}
                       Analyze festival-wise demand impact.
                    """

    response = llm.invoke([
        SystemMessage(content=system_prompt),
        HumanMessage(content=human_prompt)
    ])
     

    
    return response.festivals