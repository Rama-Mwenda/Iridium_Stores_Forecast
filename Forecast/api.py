import numpy as np
np.float_ = np.float64
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
from typing import List 
from datetime import datetime
from prophet.serialize import model_from_json
import json


app = FastAPI()


# Load the saved models dictionary from the JSON file
def load_model(instance: str):
    '''
    function to load model from the models.json file based on user input
    '''
    try:
        with open('models.json', 'r') as f:
            models = json.load(f)

        # Load a specific model from the dictionary
        if instance in models:
            model = model_from_json(models[instance])
            print('--Model loaded successfully--')
            return model
        else:
            raise ValueError(f"Model for instance '{instance}' not found.")
    except Exception as e:
        print(f'--Error loading the model: {str(e)}--')
        return None

    
def get_key(category_id=None, store_id=None):
    """
    Returns a specified string as a dictionary key.
    If one of them is not available, returns the available one.
    """
    if category_id and store_id:
        return f"comb_model"
    elif category_id:
        return category_id
    elif store_id:
        return store_id
    else:
        return None  # or any other default value

    
    
#Request and Check User input    
class Request(BaseModel):
    date: datetime
    store_id: str = None # Default to None
    category_id: str = None
    onpromotion: int
    nbr_of_transactions: int
    forecast_days: int = 56  # Default to 8 weeks


@app.get("/")
async def read_root():
    return {"STATUS: OK": "API is online"}


@app.post("/forecast")
async def forecast(request: Request):
    instance = get_key(request.category_id, request.store_id)
    
    # Load model
    model = load_model(instance=instance)
    
    if model is None:
        raise HTTPException(status_code=404, detail="Model not found for the specified instance.")
    
    # Determine the frequency of the model (daily or weekly)
    if instance == 'comb_model':
        freq = 'W'  # Weekly frequency for comb_model
    else:
        freq = 'D'  # Daily frequency for other models
    
    
    # Create a dataframe for forecasting
    future = pd.DataFrame({
        "ds": pd.date_range(start=request.date, periods=request.forecast_days, freq=freq),
        "onpromotion": [request.onpromotion] * request.forecast_days if request.onpromotion is not None else None,
        "nbr_of_transactions": [request.nbr_of_transactions] * request.forecast_days if request.nbr_of_transactions is not None else None
    })
    
    
    # Remove timezone information from the 'ds' column
    future['ds'] = future['ds'].dt.tz_localize(None)

    # Make predictions
    try:
        forecast = model.predict(future)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during prediction: {str(e)}")

    # Return the forecast dataframe
    return forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]].to_dict(orient="records")
