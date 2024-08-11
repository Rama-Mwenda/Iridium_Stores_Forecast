import streamlit as st
import streamlit.components.v1 as components


# Redirect to login page if user is not authenticated
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("You need to log in to access this page.")
    st.stop()

# Set the page configuration (optional)
st.set_page_config(page_title="Iridium Dashboard", layout="wide")

# Embed the Power BI dashboard using the iframe
st.markdown("## Iridium Dashboard")

# The iframe HTML code to embed the Power BI dashboard
iframe_code = """
<iframe title="Iridium Dashboard" width="1140" height="541.25" 
        src="https://app.powerbi.com/reportEmbed?reportId=c283cf4c-f99d-40ff-845a-010d4f78064b&autoAuth=true&ctid=4487b52f-f118-4830-b49d-3c298cb71075" 
        frameborder="0" allowFullScreen="true"></iframe>
"""

# Display the iframe in the Streamlit app
components.html(iframe_code, height=550, width=1150)
