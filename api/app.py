from fastapi import FastAPI
import joblib
import pandas as pd
from pydantic import BaseModel


app = FastAPI()


class store_features(BaseModel):
    # Enter the features and their dtype
    # feature: dtype


# define the api entry point function
@app.get('/')
def root():
    return {"Status": "Iridium Stores API is Online ..."}


# import the model
pipeline = joblib.load('../api/models/.joblib')


# this fuction sends the forecasted result back to the api server
@app.post('/forecast')
def sales_forecast(data: store_features):
    