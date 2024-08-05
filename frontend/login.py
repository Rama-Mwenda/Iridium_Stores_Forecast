import streamlit as st
import streamlit_authenticator as stauth
from streamlit_authenticator.utilities import LoginError, CredentialsError, ResetError

def show_login(config):
    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
        config['pre-authorized']
    )
    
    # Login Form
    st.subheader("Login")
    try:
        authenticator.login()
    except LoginError as e:
        st.error(e)

    if st.session_state["authentication_status"]:
        st.success(f'Welcome *{st.session_state["name"]}*')
        # Set a session state variable to indicate successful login
        st.session_state['logged_in'] = True
        # Redirect to the main page (or any other page)
        st.experimental_rerun()  # This triggers a rerun of the script
    elif st.session_state["authentication_status"] is False:
        st.error('Username/password is incorrect')
    elif st.session_state["authentication_status"] is None:
        st.warning('Please enter your username and password')

    # Show Reset Password option if user fails to login or asks for it
    if st.session_state["authentication_status"] is False or st.button("Forgot Password?"):
        st.subheader("Reset Password")
        try:
            if authenticator.reset_password(st.text_input("Enter your username")):
                st.success('Password modified successfully')
        except ResetError as e:
            st.error(e)
        except CredentialsError as e:
            st.error(e)