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


# Make sure the button is initially disabled
st.session_state.button_disabled = True

# Tracks the path the user has chosen, to avoid creating 2 choose_files pages
st.session_state.local_upload = True

# Resets this variable if the user goes back to repository naming
st.session_state.has_uploaded = False
#################################################################################
#################################################################################
#################################################################################

# Set up page configuration and load CSS styles
st.set_page_config(
    page_title="Repository Creation",
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
    st.switch_page("pages/choose_new_repos.py")

if st.button("🔄"):
    st.rerun()

############################################################################################
############################################################################################
############################################################################################
cols1, cols2 = st.columns([1, 1])
with cols1:
    st.image(
        "https://closer.pt/wp-content/uploads/2024/03/Closer_white.svg", width=250)
# Format both the start and end dates by taking the first 10 characters

# Spacer between logo and metrics
st.write("")

############################################################################################
################################ CODE ######################################################
############################################################################################

# Database creation
st.markdown("<h1 style='text-align: center;'>Create a repository</h1>",
            unsafe_allow_html=True)
database_name = st.text_input("Enter a name for the new repository:")

if database_name in st.session_state.object.get_all_repos():
    st.warning("Repository already exists")
    st.session_state.button_disabled = True

else:
    if len(database_name) > 0:
        st.success("The name is valid, you may proceed")
        st.session_state.button_disabled = False


# Lets user know that the branch is being created after clicking the button
with st.spinner("Creating new repo...", show_time=True):

    if st.button("Create new repository", disabled=st.session_state.button_disabled):
        # Logic for creating the new database can go here
        st.session_state.object.create_repository(
            database_name, description="")

        st.switch_page("pages/local_upload.py")

# Debugging
# if st.button("MOVE ON FOR TESTING!!!"):
#    st.switch_page("pages/local_upload.py")

st.divider()  # Adds a horizontal line as a separator
