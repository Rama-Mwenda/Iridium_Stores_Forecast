# %%
#import libraries
import numpy as np
np.float_ = np.float64 #Avoid Prophet numpy version error

import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, mean_absolute_percentage_error
from prophet.serialize import model_to_json, model_from_json
import json
from sklearn.preprocessing import LabelEncoder
import pickle


print('libraries loaded successfuly')

# %%
# Read in data
df = pd.read_csv('train_clean.csv', parse_dates=True).drop('Unnamed: 0', axis=1)
df['date'] = pd.to_datetime(df['date'])
df['date'] = df['date'] + pd.DateOffset(years=100) #Avoids Errno2 when dumping model
df




#%%
#define empty dictionary for all the models
models = {}
mape_rmse_dict = {}




# %%
# Shift the date range forward by 100 years

# Run the model for each category in a loop
for product in df['category_id'].unique():
    #Groupby product to get product performance forecast 
    product_df = df.groupby(['date','category_id']).sum().drop('store_id', axis=1).reset_index()
    
    # Filter the data for the current category, set date as index and sort
    product_df_filtered = product_df[product_df['category_id'] == product].sort_values(by='date')

    # Get the number of unique dates
    unique_dates = product_df_filtered['date'].unique()

    # Calculate the split point (80% for training, 20% for validation)
    split_index = int(len(unique_dates) * 0.8)

    # Determine the date corresponding to the split index
    split_date = unique_dates[split_index]

    # Split the data
    train = product_df_filtered[product_df_filtered['date'] <= split_date]
    test = product_df_filtered[product_df_filtered['date'] > split_date]

    # Data Preparation for Prophet
    train_df = train.reset_index()[['date', 'target','onpromotion','nbr_of_transactions']].rename(columns={'date': 'ds', 'target': 'y'})
    eval_df = test.reset_index()[['date','target','onpromotion','nbr_of_transactions']].rename(columns={'date': 'ds', 'target': 'y'})

    # Initialize the Prophet model
    model = Prophet()

    # If you have additional regressors (like promotions), you need to add them to the model separately
    model.add_regressor('onpromotion')
    model.add_regressor('nbr_of_transactions')

    # Fit the model
    model.fit(train_df)

    # Create a dataframe for predictions on the validation set
    future_val = eval_df[['ds', 'onpromotion', 'nbr_of_transactions']]

    # Make predictions
    forecast_val = model.predict(future_val)
    forecast_val['ds'] = forecast_val['ds'] - pd.DateOffset(years=100) #remove date offset

    # Calculate RMSE
    rmse = np.sqrt(mean_squared_error(eval_df['y'], forecast_val['yhat']))
   
    # Calculate MAPE
    mape = mean_absolute_percentage_error(eval_df['y'], forecast_val['yhat'])
    
    # Save the MAPE and RMSE values to the dictionary
    mape_rmse_dict[product] = {'MAPE': mape, 'RMSE': rmse}

    # Optional: Plot the forecast
    fig = model.plot(forecast_val)
    ax = fig.gca()

    # Add the actual data points
    ax.plot(eval_df['ds'], eval_df['y'], 'r.', label='Actual')

    # Add legend
    plt.legend()

    # Show plot
    plt.title(product)
    plt.show()

    # Save the model to the dictionary
    instance = product
    model_dict = model_to_json(model)
    models[instance] = model_dict

with open('models.json', 'w') as f:
    json.dump(models, f)









# %%

#Groupby store to get store performance forecast 
store_df = df.groupby(['date','store_id']).sum().drop('category_id', axis=1).reset_index()

# Run the model for each category in a loop
for store in store_df['store_id'].unique():
    
    # Filter the data for the current category, set date as index and sort
    store_df_filtered = store_df[store_df['store_id'] == store].sort_values(by='date')

    # Get the number of unique dates
    unique_dates = store_df_filtered['date'].unique()

    # Calculate the split point (80% for training, 20% for validation)
    split_index = int(len(unique_dates) * 0.8)

    # Determine the date corresponding to the split index
    split_date = unique_dates[split_index]

    # Split the data
    train = store_df_filtered[store_df_filtered['date'] <= split_date]
    test = store_df_filtered[store_df_filtered['date'] > split_date]

    # Data Preparation for Prophet
    train_df = train.reset_index()[['date', 'target','onpromotion','nbr_of_transactions']].rename(columns={'date': 'ds', 'target': 'y'})
    eval_df = test.reset_index()[['date','target','onpromotion','nbr_of_transactions']].rename(columns={'date': 'ds', 'target': 'y'})

    # Initialize the Prophet model
    model = Prophet()

    # If you have additional regressors (like promotions), you need to add them to the model separately
    model.add_regressor('onpromotion')
    model.add_regressor('nbr_of_transactions')

    # Fit the model
    model.fit(train_df)

    # Create a dataframe for predictions on the validation set
    future_val = eval_df[['ds', 'onpromotion', 'nbr_of_transactions']]

    # Make predictions
    forecast_val = model.predict(future_val)
    forecast_val['ds'] = forecast_val['ds'] - pd.DateOffset(years=100) #remove date offset

    # Calculate RMSE
    rmse = np.sqrt(mean_squared_error(eval_df['y'], forecast_val['yhat']))
   
    # Calculate MAPE
    mape = mean_absolute_percentage_error(eval_df['y'], forecast_val['yhat'])
    
    # Save the MAPE and RMSE values to the dictionary
    mape_rmse_dict[store] = {'MAPE': mape, 'RMSE': rmse}

    # Optional: Plot the forecast
    fig = model.plot(forecast_val)
    ax = fig.gca()

    # Add the actual data points
    ax.plot(eval_df['ds'], eval_df['y'], 'r.', label='Actual')

    # Add legend
    plt.legend()

    # Show plot
    plt.title(store)
    plt.show()

    # Save the model to the dictionary
    instance = store
    model_dict = model_to_json(model)
    models[instance] = model_dict

with open('models.json', 'w') as f:
    json.dump(models, f)






# %%
# Run the model for all categories and store in a loop
df_resampled = df.resample('W', on='date').sum().drop(columns=['store_id','category_id']).reset_index()

# Define the features to use in the model
features = ['date', 'onpromotion', 'nbr_of_transactions']

# Define the target variable
target = 'target'

# Split the data into training and testing sets
train_size = int(len(df_resampled) * 0.8)
train_df = df_resampled[:train_size]
test_df = df_resampled[train_size:]

# Create the Prophet model
model = Prophet()

# Add additional regressors
model.add_regressor('onpromotion')
model.add_regressor('nbr_of_transactions')

# Fit the model to the training data
model.fit(train_df[features + [target]].rename(columns={'date': 'ds', target: 'y'}))

# Make predictions on the testing data
forecast = model.predict(test_df[features].rename(columns={'date': 'ds'}))
forecast['ds'] = forecast['ds'] - pd.DateOffset(years=100) #remove date offset

# Evaluate the model using RMSE and MAPE
rmse = np.sqrt(mean_squared_error(test_df[target], forecast['yhat']))
mape = mean_absolute_percentage_error(test_df[target], forecast['yhat'])

# Save the MAPE and RMSE values to the dictionary
mape_rmse_dict['comb_model'] = {'MAPE': mape, 'RMSE': rmse}

# Save the model to the dictionary
instance = 'comb_model'
model_dict = model_to_json(model)
models[instance] = model_dict

with open('models.json', 'w') as f:
    json.dump(models, f)






# %%
def load_model():
    try:
        with open('models.json', 'r') as f:
            models = json.load(f)
            
        # Load a specific model from the dictionary
        model = model_from_json(models['category_1'])
        print('--Model loaded successfully--')
    except Exception as e:
        print(f'--Error loading the models: {str(e)}--')
        return None

# %%
# assuming mape_rmse_dict is your dictionary
dx = pd.DataFrame(mape_rmse_dict).T
dx = dx.map(lambda x: round(x, 2))

# remove scientific notation
pd.options.display.float_format = '{:.2f}'.format
print(dx)
# %%
df_resampled
# %%
