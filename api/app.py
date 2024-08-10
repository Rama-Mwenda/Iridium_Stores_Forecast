# from fastapi import FastAPI
# import joblib
# import pandas as pd
# from pydantic import BaseModel


# app = FastAPI()


# class store_features(BaseModel):
#     # Enter the features and their dtype
#     # feature: dtype


# # define the api entry point function
# @app.get('/')
# def root():
#     return {"Status": "Iridium Stores API is Online ..."}


# # import the model
# prophet_pipeline = joblib.load('../api/models/prophet.pkl')
# sarima_pipeline = joblib.load('../api/models/sarima.pkl')

# # this fuction sends the forecasted result back to the api server
# @app.post('/prophet_forecast')
# def forecast_sales_prophet(data: store_features):
#     df = pd.DataFrame([data.model_dump()])
#     prediction = prophet_pipeline.predict(df)
#     int_features = int(prediction[0])
#     # label = encoder.inverse_transform([int_features])[0]
#     probability = round(float(prophet_pipeline.predict_proba(df)[0][int_features])*100, 2)
#     final_prediction = {"prediction": label, "probability": probability}
#     return {"final_prediction": final_prediction}


# @app.post('/rf_predict')
# def predict_sepsis_rf(data: sepsis_features):
#     df = pd.DataFrame([data.model_dump()])
#     rf_prediction = forest_pipeline.predict(df)
#     int_features = int(rf_prediction[0])
#     label = encoder.inverse_transform([int_features])[0]
#     probability = round(float(forest_pipeline.predict_proba(df)[0][int_features])*100, 2)
#     final_prediction = {"prediction": label, "probability": probability}
#     return {"final_prediction": final_prediction}
    


from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import pickle
import joblib

# Load the Prophet model from the provided file
prophet_pipeline = joblib.load('../api/models/prophet.pkl')

app = FastAPI()

# Define the expected input data format
class DateFeatures(BaseModel):
    date: str  # Assuming the input will be a date string in 'YYYY-MM-DD' format

@app.post('/prophet_predict')
def predict_with_prophet(data: DateFeatures):
    # Convert the input data to a DataFrame
    df = pd.DataFrame([{'ds': data.date}])

    # Make predictions using the loaded Prophet model
    forecast = prophet_pipeline.predict(df)
    
    # Extract the prediction and its components
    prediction = forecast['yhat'].iloc[0]
    lower_bound = forecast['yhat_lower'].iloc[0]
    upper_bound = forecast['yhat_upper'].iloc[0]

    # Prepare the final output
    final_prediction = {
        "prediction": prediction,
        "lower_bound": lower_bound,
        "upper_bound": upper_bound
    }
    
    return {"final_prediction": final_prediction}