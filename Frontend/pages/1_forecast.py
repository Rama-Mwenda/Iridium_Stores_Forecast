import streamlit as st
import requests
import time
import pandas as pd
from datetime import datetime
import numpy as np
from PIL import Image
import base64
import io


# Redirect to login page if user is not authenticated
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("You need to log in to access this page.")
    st.stop()


# Set page config to be wide
st.set_page_config(
    layout="wide",
    page_title="Predict",
    page_icon="",
    initial_sidebar_state="expanded",
    menu_items=None
)


st.title('Why Forecast Sales?')


st.write(f"By leveraging machine learning algorithms to forecast sales, businesses can unlock unprecedented accuracy and reliability,\n"
         f"enabling informed decision-making and strategic planning that drives revenue growth and competitiveness.\n")
st.write(f"ML-powered sales forecasting can also identify hidden patterns and trends, revealing new opportunities for optimization and improvement.\n" 
         f"Ultimately, this leads to increased profitability, reduced inventory costs, and enhanced customer satisfaction giving businesses a critical edge in today's fast-paced market.")
st.write(f"Want to see how it works? Try out our interactive sales forecasting tool below and discover for yourself in real time!")


st.title('Training Data Used')
# Create a markdown element with the HTML code
st.markdown("""
<style>
    .column {
        width: 24%;
        padding: 20px;
        display: inline-block;
    }
    .container {
        width: 100%;
        text-align: center;
    }
    .heading {
        font-family: Helvetica;
        font-size: 15pt;
        font-weight: bold;
        background-color: #1e3d67;
        color: white
    }
    .spacer {
        height: 30px;
    }
</style>

<div class="column">
    <div class="container">
        <p class="heading">On Promotion</p>
    </div>
    <div class="container">
        <p>The number of products per category that were being promoted on a particular date.</p>
    </div>
</div>

<div class="column">
    <div class="container">
        <p class="heading">No. of Transactions</p>
    </div>
    <div class="container">
        <p>The total number of transactions that occured on a particular store at a particular date.</p>
    </div>
</div>

<div class="column">
    <div class="container">
        <p class="heading">Category ID</p>
    </div>
    <div class="container">
        <p>The unique label given to a group of products that have been categorized by their similarities.</p>
    </div>
</div>

<div class="column">
    <div class="container">
        <p class="heading">Store ID</p>
    </div>
    <div class="container">
        <p>The unique identifier for each of the stores under the Irridium group of grocery stores.</p>
    </div>
</div>
""", unsafe_allow_html=True)


st.markdown("""
<div style="text-align:center; 
font-family: Helvetica; 
font-style: italic; 
font-weight: bold;
color: red; 
font-size: 26px;
cursor: pointer;">
Try it out Yourself!
</div>

<div class="spacer"></div>

""", unsafe_allow_html=True)

st.warning('The model was trained with data from 1900 - 1902. That is why we have set the maximum to be 100 years prediction')


#limit dates for correct predictions
min_date = pd.to_datetime('1900-01-01')
max_date = pd.to_datetime('1999-12-31')


with st.form('forecast_form'):
    cola, colb, colc= st.columns(3)
    with cola:
        store = st.slider('Select Store ID ', min_value=None, max_value=54)
        onpromotion = st.number_input('Enter number of onpromotion (optional)', min_value=0, step=1)
    with colc: 
        category = st.slider('Select Category ID', min_value=None, max_value=33)
        nbr_of_transactions = st.number_input('Enter number of Transactions (optional)', min_value=0, step=1)
    with colb:
        date = st.date_input("Select a start date:", min_value=min_date, max_value=max_date)
        forecast_days = st.number_input('How many days do you want to forecast?', min_value=7, step=1)
    
    left, center, right = st.columns(3)
    with center:
        submitted = st.form_submit_button(label='Run the Model', use_container_width=True)


#prediction count
if 'prediction_count' not in st.session_state:
    st.session_state['prediction_count'] = 0

with right:
    st.markdown(f"<p style='text-align: right;'>Number of Predictions Made: {st.session_state['prediction_count']}</p>", unsafe_allow_html=True)
    
#forecast
if submitted:
    # Increment the prediction count
    st.session_state['prediction_count'] += 1
    
    selected_date = date.strftime("%Y-%m-%d")
    
    # Your code here to handle the form submission
    form_values = {
        "date": selected_date,
        "store_id": (f"store_{store}"),
        "onpromotion": onpromotion,
        "category_id": (f"category_{category}"),
        "nbr_of_transactions": nbr_of_transactions,
        "forecast_days": forecast_days
    }
    
    
    with st.spinner('Checking that all systems are online...'):
        time.sleep(2)

    # Pass the form values to your API
    response = requests.get("https://iridium-stores.onrender.com")

    if response.status_code == 200:
        with left:
            st.success("Server is online")
            time.sleep(1)
        with st.spinner('Running Predictions...'):
            time.sleep(2)
            
        forecast_response = requests.post("https://iridium-stores.onrender.com/forecast", json=form_values)
        
        if forecast_response.status_code == 200:
            forecast_data = forecast_response.json()
            # Assuming forecast_data is a list of dictionaries
            forecast_df = pd.DataFrame(forecast_data)
            with st.spinner('Analysing Server Response...'):
                time.sleep(2)
            with st.spinner('Generating Forecasts...'):
                time.sleep(2)
            with st.spinner('Finalizing...'):
                time.sleep(2)
            
            st.title('Predicted data')
            st.dataframe(forecast_df, use_container_width=True)
            
            st.markdown(f"""
                <div style="height: 20px;"></div>
                <hr class="divider">
            """, unsafe_allow_html=True)

            # Define the values for the buttons
            max = f"{forecast_df['yhat'].max():,.2f}"
            average = f"{forecast_df['yhat'].mean():,.2f}"
            min = f"{forecast_df['yhat'].min():,.2f}"

            # Create two columns with different widths
            col1, col2 = st.columns((2, 1))

            # Add content to the left column (2/3 width)
            with col1:
                # Create a title with the forecast days
                st.title(f"Forecast for the next {forecast_days} days")

                # Display the chart
                st.bar_chart(forecast_df, x='ds', y='yhat')
                
                
            # Add content to the right column (1/3 width)
            with col2:
                st.title("")
                
                # Create the metrics
                st.button("Anticipated Maximum", use_container_width=True)
                
                st.markdown(f"""
                <div style="text-align: center">
                <span style="font-family: Helvetica; font-size: 30pt; color: red">{max}</span>
                </div>
            """, unsafe_allow_html=True)
                
                st.button("Expected Average", use_container_width=True)
                
                st.markdown(f"""
                <div style="text-align: center">
                <span style="font-family: Helvetica; font-size: 30pt; color: red">{average}</span>
                </div>
            """, unsafe_allow_html=True)
                
                st.button("Tolerable Minimum", use_container_width=True)
                
                st.markdown(f"""
                <div style="text-align: center">
                <span style="font-family: Helvetica; font-size: 30pt; color: red">{min}</span>
                </div>
            """, unsafe_allow_html=True)
            
        else:
            st.error(f"Error running forecast: {forecast_response.text}")
    else:
        st.error("Error connecting to the server, Please Try again.")
        
        

st.markdown(f"""
    <div style="height: 20px;"></div>
    <hr class="divider">
""", unsafe_allow_html=True)


# Add a new section for the creator

# Open the image and encode it to base64
image = Image.open('Creator.jpeg')
buffered = io.BytesIO()
image.save(buffered, format="JPEG")
img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")


st.markdown(f"""
<div style="background-color: ; padding: 20px; border-radius: 10px">
    <h3 style="color: ; text-align: center; font-family: Helvetica; font-weight: bold">This webapp was proudly developed by:</h3>
    <div style="text-align: center">
        <img src="data:image/jpeg;base64,{img_str}" alt="Creator Photo" style="border-radius: 50%; width: 200px; height: 200px; margin-bottom: 20px">
    </div>
    <div style="text-align: center; color: white; margin-top: 20px">
        <a href="https://www.linkedin.com/in/Rama-Mwenda/" target="_blank" style="text-decoration: none; color:; margin-right: 20px">
            <img src="https://cdn2.iconfinder.com/data/icons/popular-social-media-flat/48/Popular_Social_Media-22-512.png" alt="LinkedIn Logo" width="32" height="32">
            <i class="fa fa-linkedin" aria-hidden="true"></i> <span style="color:">LinkedIn</span>
        </a>
        <a href="https://github.com/Rama-Mwenda" target="_blank" style="text-decoration: none; color:; margin-right: 20px">
            <img src="https://github.com/fluidicon.png" alt="GitHub Logo" width="32" height="32">
            <i class="fa fa-github" aria-hidden="true"></i> <span style="color:">GitHub</span>
        </a>
        <a href="https://medium.com/@ngige.mwenda" target="_blank" style="text-decoration: none; color:; margin-right: 20px">
            <img src="https://cdn.icon-icons.com/icons2/3041/PNG/512/medium_logo_icon_189223.png" alt="Medium Logo" width="32" height="32">
            <i class="fa fa-medium" aria-hidden="true"></i> <span style="color:">Medium</span>
        </a>
        </a>
        <a href="mailto:ngige.mwenda@outlook.com" target="_blank" style="text-decoration: none; color: ">
            <img src="https://clipartcraft.com/images/outlook-logo-ico-9.png" alt="Outlook Logo" width="32" height="32">
            <i class="fa fa-medium" aria-hidden="true"></i> <span style="color: ">Email</span>
        </a>
    </div>
</div>
""", unsafe_allow_html=True)