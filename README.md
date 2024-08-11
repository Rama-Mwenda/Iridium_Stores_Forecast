## IRIDIUM STORES - SALES FORECAST APP

### About
Iridium stores is a chain of grocery stores based in Wakanda. 

### Business Objective
The objective is to create an application that can be used by the individual chain stores to predict the quantity of products they will sell for at least eight weeks.

The company management needs to be able to forecast the number of products that will be required for all the stores per week for at least eight weeks, for grocery stores located in different areas. This allows the management to budget and prepare for the future.

The management also needs to know how many products will be required in each store.

### Methodology
We have employed the use of Cross Industry Standard Proces for Data Mining (CRISP-DM) Methodology as the Business Intelligence(BI) Team for Iridium Stores.

### Success Criteria and Definition of Done
1. The application should be able to forecast the number of products to be sold per week, per store and in total for at least 2 months.
2. The Application should have at least two endpoints. One for the management of Iridium Stores and another for the Store Manager at the chain store. 
 
 **Store Manager Endpoint Features** 
 1. No access to prediction
 2. EDA dashboard
 3. Secure Login

 **Management Endpoint Features**
 1. Access to prediction
 2. EDA Dashboard
 3. Forecast Dashboard
 4. Secure Login

### Stakeholders
1. Management 
2. Store Manager
3. Business Intelligence(BI) Team

### Communication Plan
1. The Business Intelligence (BI) Team will communicate with the management at least once a week
2. The Business Intelligence(BI) Team will communicate with the Store Manager at least three times a week.
3. The BI Team will meet daily via TEAMS virtual meeting

### Available Data
The company has provide the Business Intelligence team with Annonymised data for 33 products from 54 stores in different locations across the country. 

| ***The Data Dictionary*** |
| --------------------------- |
| **Column Name** | **Description** |
| *Target* | the total sales for a product category at a particular store at a given date |
| *Stores_id* | the unique store id |
| *Category_id* | the unique Product category id |
| *Date* | date in numerical representation |
| *Onpromotion* | gives the total number of items in a Product category that were being promoted at a store at a given date |
| *Nbr_of_transactions* | the total number of transactions happened at a store at a given date |
| *year_weekofyear* | the combination of the year and the week of the year, (year_weekofyear = year*100+week_of_year) |
| *ID* | the unique identifier for each row in the testing set: year_week_{year_weekofyear}_{store_id}_{Category_id} |
