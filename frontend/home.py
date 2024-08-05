import streamlit as st
from utils import load_config
import login
import signup

# Set page configuration
st.set_page_config(page_title='Sales Forecast', layout='wide')

# Load configuration
config = load_config()

# Navigation Menu
menu = ["Login", "Sign Up"]
choice = st.sidebar.selectbox("Menu", menu)

# Route to the appropriate page
if choice == "Login":
    login.show_login(config)
elif choice == "Sign Up":
    signup.show_signup(config)