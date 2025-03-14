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
    st.session_state.branch = st.session_state.to_upload

# The main branch was used previously, no need to fetch it again
main_branch = st.session_state.repo_contents

#################################################################################
#################################################################################
#################################################################################

# Set up page configuration and load CSS styles
st.set_page_config(
    page_title="Final Review",
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

# Inject custom CSS for box with an outline
st.markdown("""
    <style>
        .box-with-outline {
            border: 2px solid #A9A9A9;  /* Gray border */
            padding: 20px;
            border-radius: 10px;  /* Optional: rounded corners */
            font-size: 20px;  /* Increase font size */
            text-align: center;  /* Center the text */
        }
    </style>
""", unsafe_allow_html=True)

###########################################################################
######################## CODE #############################################
###########################################################################

with st.container():
    # Centered title
    st.markdown("<h1 style='text-align: center;'>Final comparison</h1>",
                unsafe_allow_html=True)
    st.markdown("<h5 style='text-align: center;'>Submit to create a pull request</h5>",
                unsafe_allow_html=True)
    st.divider()  # Adds a horizontal line as a separator

#################################################################################################
#################################################################################################
#################################################################################################


# Placement of the selectbox
left1, middle1, right1 = st.columns([2, 2, 1])

# Remove the current branch from the options and create a dropdown
options = st.session_state.object.get_all_branches()
# Remove both the current branch (permanent) and the main branch (temporary)
options.remove(st.session_state.object.current_branch)
options.remove('main')
# Making sure these are the first 2 options
final_options = ['Choose a branch...', 'main'] + options

with left1:
    # st.markdown(f'<div class="box-with-outline">Current branch is \n'
    #             f'{st.session_state.object.current_branch}</div>',
    #             unsafe_allow_html=True)
    pr_name = st.text_input("Enter the name of the PR:",
                            label_visibility="collapsed",
                            value='Enter a name for the PR...')


with middle1:
    # Dropdown for PR specification
    target = st.selectbox("Choose the target branch:",
                          [option for option in final_options], label_visibility="collapsed")

if target != 'Choose a branch...' and pr_name != 'Enter a name for the PR...':
    st.session_state.button_disabled = False

with right1:
    if st.button("Submit for Pull Request", disabled=st.session_state.button_disabled):
        try:
            st.session_state.object.create_pull_request(base_branch=target, head_branch=st.session_state.new_branch,
                                                        title=pr_name, body='Approve migration')
            st.switch_page("pages/logout.py")

        except Exception as e:
            error_message = str(e)
            st.warning(f"⚠️ {error_message} The possible problems are: \n"
                       f"- no commits/changes between these branches (code migration problem); \n"
                       f"- PR already active (wait for approval)")

st.divider()  # Adds a horizontal line as a separator

# Placement of the selectbox
p1, p2, p3 = st.columns([0.5, 2, 1])
with p2:
    # Display the list of files
    selected_file = st.selectbox(
        f"Browse the files from: {st.session_state.object.current_repo.name}", [file['path'] for file in st.session_state.branch])

# Create two columns, one for the file selection, and one for the content display
# 1 part for the left column (file chooser), 2 parts for the right column (content display)
col1, col2, col3 = st.columns([2, 0.05, 2])

# In the left column
with col1:
    # Show the content of the selected file
    if selected_file:
        with st.expander(f"Click to view {selected_file}"):

            file_data = next(
                (file for file in main_branch if file['path'] == selected_file), None)
            if file_data:
                # Display file content inside a larger white box
                st.code(file_data['content'])

with col2:
    st.markdown(
        """
        <div style="height: 100vh; border-left: 2px solid #ccc; margin: auto;"></div>
        """,
        unsafe_allow_html=True
    )  # Vertical divider

# In the right column (content display)
with col3:
    # Show the content of the selected file
    if selected_file:
        with st.expander(f"Click to view {selected_file}"):
            file_data = next(
                (file for file in st.session_state.branch if file['path'] == selected_file), None)
            if file_data:
                # Display file content inside a larger white box
                st.code(file_data['content'])

# if st.button("MOVE ON FOR TESTING!!!"):
#     st.switch_page("pages/logout.py")
