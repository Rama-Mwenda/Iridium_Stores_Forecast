# %%

#import libraries
import numpy as np
np.float_ = np.float64

import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, mean_absolute_percentage_error

print('libraries loaded successfuly')

# %%
# Read in data
df = pd.read_csv('train_clean.csv', parse_dates=True).drop('Unnamed: 0', axis=1)
df['date'] = pd.to_datetime(df['date'])

#groupby product to get product performance forecast 
product_df = df.groupby(['date','category_id']).sum().drop(['store_id'], axis=1).reset_index()
pd.to_datetime(product_df['date'])
product_df
# %%
#Model and predict for each category in a loop 
for product in product_df['category_id'].unique():
    product_df_filtered = product_df[product_df['category_id'] == product]

product_df_filtered

# Set the Date as index
product_df_filtered.set_index('date', inplace=True)

#split to train and validation sets
train = product_df_filtered[:'1902-06-15']
test = product_df_filtered['1902-06-16':]

train
# %% 
#Data Preparation for Prophet
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

# Calculate RMSE
rmse = np.sqrt(mean_squared_error(eval_df['y'], forecast_val['yhat']))
print(f'RMSE: {rmse:.2f}')

# Calculate MAPE
mape = mean_absolute_percentage_error(eval_df['y'], forecast_val['yhat'])
print(f'MAPE: {(mape * 100):.2f}%')

# Optional: Plot the forecast
fig = model.plot(forecast_val)
ax = fig.gca()

# Add the actual data points
ax.plot(eval_df['ds'], eval_df['y'], 'r.', label='Actual')

# Add legend
plt.legend()

# Show plot
plt.show()

# %%
