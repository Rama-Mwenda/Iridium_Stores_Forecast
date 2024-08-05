# %%
#Imports
import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX
import matplotlib.pyplot as plt
import numpy as np

print('models imported successfully')
# %%
# Read in data
df = pd.read_csv('train_clean.csv', parse_dates=True).drop('Unnamed: 0', axis=1)
df['date'] = pd.to_datetime(df['date'])

#groupby product to get product performance forecast 
product_df = df.groupby(['date','category_id']).sum().drop(['store_id','nbr_of_transactions'], axis=1).reset_index()
product_df
# %%
#Model and predict for each category in a loop 
for product in product_df['category_id'].unique():
    product_df_filtered = product_df[product_df['category_id'] == product]

product_df_filtered

# Set the Date as index
product_df_filtered.set_index('date', inplace=True)

# %%

# Split data into train and test sets
train = product_df_filtered[:'1902-06-15']
test = product_df_filtered['1902-06-16':]

# Build and train the SARIMA model
model = SARIMAX(train['target'], exog=train[['onpromotion']], order=(1, 1, 1), seasonal_order=(1, 1, 1, 7))
model_fit = model.fit(disp=False)

# Forecast
forecast = model_fit.predict(start=len(train), end=len(train) + len(test) - 1, exog=test[['onpromotion']])

# Evaluate
rmse = ((forecast - test['target']) ** 2).mean() ** 0.5
print('RMSE: ', rmse)

# Plot the results
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 5))
#plt.plot(train['target'], label='Train')
plt.plot(test['target'], label='Test')
plt.plot(forecast, label='Forecast')
plt.legend()
plt.show()
# %%
ape = np.abs((test['target'] - forecast)/test['target'])*100
mape = np.mean(ape)
print(f'{mape:.2f}%')

# %%
