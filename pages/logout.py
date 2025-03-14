import streamlit as st
import pandas as pd
from github_connector import connector_github
from streamlit_tree_select import tree_select
import time

#################################################################################
###################### SESSION_STATE ############################################
#################################################################################

# Triggers if the session state is lost, basically whenever you reload the page
if "object" not in st.session_state:
    st.warning("You need to log in again. Redirecting...")
    time.sleep(2)
    st.switch_page("homepage.py")

# Make sure the button is initially disabled
st.session_state.button_disabled = True
#################################################################################
#################################################################################
#################################################################################


# Set up page configuration and load CSS styles
st.set_page_config(
    page_title="Checkout",
    page_icon=(
        "https://closer.pt/wp-content/uploads/2024/04/For_ico-150x150.png"
    ),
    layout="wide"  # Ensures the layout spans the full width
)

with open(".streamlit/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

with st.sidebar:
    st.logo(
        "https://closer.pt/wp-content/uploads/2024/03/Closer_white.svg")
    st.header("Navigation")
    st.page_link("homepage.py", label="Home", icon="🏠")


############################################################################################
################################ GO BACK/REFRESH BUTTONS ###################################
############################################################################################

# Previous page redirection
# if st.button("🔙"):
#    st.switch_page("pages/final_comparison.py")
#
# if st.button("🔄"):
#    st.rerun()

#################################################################################
#################################################################################
#################################################################################

# Debugging
# st.write(f"{st.session_state.object.current_env()}")

cols1, cols2 = st.columns([1, 1])
with cols1:
    st.image(
        "https://closer.pt/wp-content/uploads/2024/03/Closer_white.svg", width=250)
# Format both the start and end dates by taking the first 10 characters

# Spacer between logo and metrics
st.write("")
###########################################################################

st.title("Code migration completed")

if st.button("Logout"):
    # Logic for creating the new database can go here
    st.session_state.object.close()
    st.switch_page("homepage.py")
