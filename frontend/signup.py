import streamlit as st
import streamlit_authenticator as stauth
from streamlit_authenticator.utilities import RegisterError
from utils import save_config

def show_signup(config):
    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
        config['pre-authorized']
    )
    
    st.subheader("Sign Up")
    try:
        email, username, name = authenticator.register_user(pre_authorization=False)
        if email:
            st.success('User registered successfully')
            # Save updated config with new user
            save_config(config)
    except RegisterError as e:
        st.error(e)