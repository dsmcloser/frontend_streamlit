import streamlit as st
import pandas as pd
from github_connector import connector_github
from streamlit_tree_select import tree_select
import unicodedata
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

if 'has_uploaded' not in st.session_state:
    st.session_state.has_uploaded = False

if 'repo_contents' not in st.session_state:
    st.session_state.repo_contents = st.session_state.object.get_all_files()

#################################################################################
#################################################################################
#################################################################################

# Set up page configuration and load CSS styles
st.set_page_config(
    page_title="Local Upload",
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
    st.switch_page("pages/new_repository.py")

if st.button("🔄"):
    st.rerun()

#################################################################################
#################################################################################
#################################################################################

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

st.title("Local Upload")

container_upload_files = st.container(border=True)


with container_upload_files:
    uploaded_files = st.file_uploader(
        "Choose a file", accept_multiple_files=True)

if not uploaded_files:
    st.session_state.button_disabled = True

else:
    st.session_state.button_disabled = False


# Lets user know that the branch is being created after clicking the button
with st.spinner("Uploading the selected files...", show_time=True):

    if st.button("Continue", disabled=st.session_state.button_disabled):

        file_list = []
        for uploaded_file in uploaded_files:
            binary_data = uploaded_file.read()
            file_dict = {  # Create a new dictionary for each file
                "path": uploaded_file.name,
                "content": binary_data.decode("utf-8", errors="replace").strip()
            }
            file_list.append(file_dict)  # Add to the list

        st.session_state.object.upload_file(
            st.session_state.repo_contents,
            file_list)

        st.session_state.repo_contents = st.session_state.object.get_all_files()
        st.session_state.has_uploaded = True
        st.switch_page("pages/choose_files.py")

    if st.session_state.has_uploaded:
        if st.button("Keep the same upload selection", disabled=False):
            st.switch_page("pages/choose_files.py")

# if st.button("MOVE ON FOR TESTING!!!"):
#    st.switch_page("pages/choose_files.py")
