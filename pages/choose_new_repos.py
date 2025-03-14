import streamlit as st
import pandas as pd
from github_connector import connector_github
import time

#################################################################################
###################### SESSION_STATE ############################################
#################################################################################

# Triggers if the session state is lost, basically whenever you reload the page
if "object" not in st.session_state:
    st.warning("You need to log in again. Redirecting...")
    time.sleep(2)
    st.switch_page("homepage.py")

# Tracks the path the user has chosen, to avoid creating 2 choose_files pages
st.session_state.local_upload = None

#################################################################################
########################## SIDEBAR AND LOGO #####################################
#################################################################################


# Set up page configuration and load CSS styles
st.set_page_config(
    page_title="Dataset Selection",
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
if st.button("🔙"):
    st.switch_page("homepage.py")

if st.button("🔄"):
    st.rerun()

#################################################################################
################################# CODE ##########################################
#################################################################################

# Debugging
# st.write(st.session_state.local_upload)

cols1, cols2 = st.columns([1, 1])
with cols1:
    st.image(
        "https://closer.pt/wp-content/uploads/2024/03/Closer_white.svg", width=250)
# Format both the start and end dates by taking the first 10 characters

# Spacer between logo and metrics
st.write("")
###########################################################################

# Debugging
# st.write(f"{st.session_state.object.current_env()}")

st.title("Are your files stored locally or on a GitHub repository?")

st.page_link("pages/new_repository.py",
             label="Locally", icon="🆕")


st.page_link("pages/repositories.py",
             label="GitHub Repository", icon="➡️")
