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


# Store the new branch in the session state, to avoid rerunning the query whenever
# the user changes the file in the select box
if st.session_state.new_branch != st.session_state.object.current_branch or 'branch' not in st.session_state:
    # Store the new branch in the session state, to avoid rerunning the query
    st.session_state.object.switch_to_branch(
        st.session_state.new_branch)
    st.session_state.branch = st.session_state.object.get_all_files()

# The main branch was used previously, no need to fetch it again
main_branch = st.session_state.repo_contents

#################################################################################
#################################################################################
#################################################################################

# Set up page configuration and load CSS styles
st.set_page_config(
    page_title="Admin Homepage",
    page_icon=(
        "https://closer.pt/wp-content/uploads/2024/04/For_ico-150x150.png"
    ),
    layout="wide"  # Ensures the layout spans the full width
)

with open(".streamlit/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

with st.sidebar:
    # st.logo(
    #     "https://closer.pt/wp-content/uploads/2024/03/Closer_white.svg")
    st.header("pages")
    st.page_link("homepage.py", label="Home", icon="🏠")

#########################################################################################
############################# GO BACK/REFRESH BUTTONS ###################################
#########################################################################################

# Previous page redirection
# if st.button("🔙"):
#     st.switch_page("pages/code_migration.py")

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
################################################################################

# Center the dropdown using CSS
st.markdown(
    """
    <style>
        .stSelectbox {
            display: flex;
            justify-content: center;
        }
        div[data-baseweb="select"] {
            width: 50% !important;  /* Adjust width */
            margin: auto;           /* Center horizontally */
        }
    </style>
    """,
    unsafe_allow_html=True,
)

###########################################################################
######################## CODE #############################################
###########################################################################

with st.container():
    # Centered title
    st.markdown("<h1 style='text-align: center;'>Final comparison</h1>",
                unsafe_allow_html=True)

    st.divider()  # Adds a horizontal line as a separator

#################################################################################################
#################################################################################################
#################################################################################################

# Placement of the selectbox
p1, p2, p3 = st.columns([0.5, 2, 1])
with p2:
    # Display the list of files
    selected_file = st.selectbox(
        f"Browse the files from: {st.session_state.object.current_repo.name}", [file['path'] for file in st.session_state.branch])

# Create two columns, one for the file selection, and one for the content display
# 1 part for the left column (file chooser), 2 parts for the right column (content display)
col1, col2, col3 = st.columns([1, 0.05, 2])

# In the left column (file selection dropdown)
with col1:
    # Show the content of the selected file
    if selected_file:
        file_data = next(
            (file for file in main_branch if file['path'] == selected_file), None)
        if file_data:
            # Display file content inside a larger white box
            st.markdown(
                f"""
                <div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px;
                            border: 1px solid #ccc; height: 400px; overflow-y: auto;
                            color: black; white-space: pre-wrap; display: flex; align-items: flex-start;">
                    <pre style="color: black; margin: 0; padding: 0; line-height: 1.2;">{file_data['content'].lstrip()}</pre>
                </div>
                """,
                unsafe_allow_html=True
            )

    # This will set a query parameter for navigation (optional, for tracking state)
    # st.experimental_set_query_params(page="after_repo_page")
#
    # Trigger a rerun to load the new page automatically
    # st.rerun()

with col2:
    st.markdown(
        """
        <div style="height: 60vh; border-left: 2px solid #ccc; margin: auto;"></div>
        """,
        unsafe_allow_html=True
    )  # Vertical divider

# In the right column (content display)
with col3:
    # Show the content of the selected file
    if selected_file:
        file_data = next(
            (file for file in st.session_state.branch if file['path'] == selected_file), None)
        if file_data:
            # Display file content inside a larger white box
            st.markdown(
                f"""
                <div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px;
                            border: 1px solid #ccc; height: 400px; overflow-y: auto;
                            color: black; white-space: pre-wrap; display: flex; align-items: flex-start;">
                    <pre style="color: black; margin: 0; padding: 0; line-height: 1.2;">{file_data['content'].lstrip()}</pre>
                </div>
                """,
                unsafe_allow_html=True
            )


if st.button("Submit for migration"):
    try:
        st.session_state.object.create_pull_request(base_branch="main", head_branch=st.session_state.new_branch,
                                                    title='PR', body='Approve migration')
        st.switch_page("pages/logout.py")

    except Exception as e:
        error_message = str(e)
        st.warning(f"⚠️ {error_message} The possible problems are: \n"
                   f"- no commits/changes between these branches (code migration problem); \n"
                   f"- PR already active (wait for approval)")

# if st.button("MOVE ON FOR TESTING!!!"):
#     st.switch_page("pages/logout.py")
