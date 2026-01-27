from sqlalchemy.orm import Session
import  pandas as pd
from prophet import Prophet
from prophet.diagnostics import cross_validation, performance_metrics
from crud import get_sales_bulk

def get_prediction(db: Session,forecast_days:int = 30):
    """ 
    get the sales history from the database and call prophet for each product
    """
    
    ## data fetch from db (type object)
    sales_data = get_sales_bulk(db,150)  
    ## sales data in ascending (if prev_id != cur_id send to prophet)
    if not sales_data:
        return {}

    prev_id = sales_data[0].product_id
    data = []
    prophet_prediction = {}
    for sale in sales_data:
            
        # if it is new id then prev id history is overed
        if(prev_id == sale.product_id):
            data.append((sale.sale_date,sale.quantity_sold))
                
                
        else:
            predicted_quantity = predict_sales_quantity(data,forecast_days,prev_id)
            prophet_prediction[prev_id] = predicted_quantity
            prev_id = sale.product_id
            data = []
            data.append((sale.sale_date,sale.quantity_sold))
            
            
    prophet_prediction[prev_id] = predict_sales_quantity(data,forecast_days,prev_id)
    return prophet_prediction
                
        
def predict_sales_quantity(data,forecast_days,id):
    """ 
    predict the forecast upward quantity for a product using prophet model with cross validation 
    """
    df = pd.DataFrame(data,columns=["ds","y"])
    df["ds"] = pd.to_datetime(df["ds"])
        
    ## atleast need 1 month data to predict
    if len(df) < 30:
        avg = df["y"].mean()
        print(f"fallback for id :{id} avg {avg} less then 30 days")
        return max(0, round(avg * forecast_days))
        
    else:
        model = Prophet(
                daily_seasonality=False,
                weekly_seasonality=True,
                yearly_seasonality=False
            )
            
        model.fit(df)
        
        try:
            df_cv = cross_validation(model,initial="60 days",horizon=f"{forecast_days} days")
            
            ## weight absolute percentage error
            wape = abs(df_cv["y"] - df_cv["yhat"]).sum() / df_cv["y"].sum()
            print(f"id {id} wape {wape}")
            if wape > 0.4:
                avg = df["y"].mean()
                print(f"fallback for id :{id} avg {avg} less then wape")
                return max(0, round(avg * forecast_days))
        except Exception as e:
            avg = df["y"].mean()
            print(f"fallback for id :{id} avg {avg} in except block {e}")
            return max(0, round(avg * forecast_days))
            
        future = model.make_future_dataframe(periods=forecast_days,freq="D")              
        prediction = model.predict(future)               
        forecast_quantity = prediction.tail(forecast_days)["yhat"].sum()
        
        return max(0, round(forecast_quantity))
    
    
