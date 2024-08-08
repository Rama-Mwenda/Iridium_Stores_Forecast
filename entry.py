import yaml
import streamlit as st
import streamlit_authenticator as stauth
from yaml.loader import SafeLoader
from streamlit_authenticator.utilities import LoginError, CredentialsError, ResetError, RegisterError


st.set_page_config(page_title="Home", page_icon="", layout="wide")

# Function to load the config file
def load_config(path='../config.yaml'):
    try:
        with open(path, 'r', encoding='utf-8') as file:
            config = yaml.load(file, Loader=SafeLoader)
            return config
    except FileNotFoundError:
        print(f"Error: The file '{path}' was not found.")
        return None
    except yaml.YAMLError as e:
        print(f"Error loading YAML file: {e}")
        return None

# Function to save the config file
def save_config(config, path='../config.yaml'):
    try:
        with open(path, 'w', encoding='utf-8') as file:
            yaml.dump(config, file, default_flow_style=False)
        print(f"Configuration successfully saved to '{path}'")
    except Exception as e:
        print(f"Error saving configuration: {e}")

# Function to show login page
def show_login(config):
    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
        config['pre-authorized']
    )
    
    # st.subheader("Login")
    try:
        authenticator.login()
    except LoginError as e:
        st.error(e)

    # Ensure session state variables are initialized
    if "authentication_status" not in st.session_state:
        st.session_state["authentication_status"] = None

    if st.session_state["authentication_status"]:
        st.success(f'Welcome *{st.session_state["name"]}*')
        authenticator.logout()
        st.session_state['logged_in'] = True 
    elif st.session_state["authentication_status"] is False:
        st.error('Username/password is incorrect')
    elif st.session_state["authentication_status"] is None:
        st.warning('Please enter your username and password')

    if st.session_state["authentication_status"] is False and st.button("Forgot Password?"):
        st.subheader("Reset Password")
        try:
            if authenticator.reset_password(st.text_input("Enter your username")):
                st.success('Password modified successfully')
        except ResetError as e:
            st.error(e)
        except CredentialsError as e:
            st.error(e)

# Function to show sign-up page
def show_signup(config):
    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
        config['pre-authorized']
    )
    
    # st.subheader("Sign Up")
    try:
        email, username, name = authenticator.register_user(pre_authorization=False)
        if email:
            st.success('User registered successfully')
            save_config(config)
    except RegisterError as e:
        st.error(e)

# Main function to run the app
def main():
    col1, col2, col3 = st.columns(3)
    with col1:
        st.title(":blue[Iridium Stores]🏬")
    with col3:
        choice = st.radio(" ", ["Login", "Sign Up"], horizontal=True)
    config = load_config()
    if config:
        if choice == "Login":
            show_login(config)
        elif choice == "Sign Up":
            show_signup(config)
    else:
        st.error("Configuration file not found. Please check the path and try again.")

if __name__ == "__main__":
    main()