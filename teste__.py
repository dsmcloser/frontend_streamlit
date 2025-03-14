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
st.session_state.local_upload = False

#################################################################################
########################## SIDEBAR AND LOGO #####################################
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


############################################################################################
################################ GO BACK/REFRESH BUTTONS ###################################
############################################################################################

# Previous page redirection
if st.button("🔙"):
    st.switch_page("pages/choose_new_repos.py")

if st.button("🔄"):
    st.rerun()

#################################################################################
########################### CODE ################################################
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

with st.container():
    databases = st.session_state.object.get_all_repos()

    # Insert the neutral option
    databases.insert('Select an option...', 0)

    # Centered title
    st.markdown("<h1 style='text-align: center;'>Select a repository to get the files from</h1>",
                unsafe_allow_html=True)

    # Centered dropdown
    selected_db = st.selectbox(
        "", databases, index=0)

    # Run the function only when the option changes (not on every rerun)
    if 'repo_contents' not in st.session_state or st.session_state.selected_option != selected_db:
        st.session_state.object.switch_to_repo(selected_db)
        st.session_state.repo_contents = st.session_state.object.get_all_files()
        # Store the selected option to avoid rerun
        st.session_state.selected_option = selected_db

    st.divider()  # Adds a horizontal line as a separator

    st.write(f"{st.session_state.object.current_env()}")

#################################################################################################
#################################################################################################
#################################################################################################

with st.container():
    if 'repo_contents' in st.session_state:
        # Create two columns, one for the file selection, and one for the content display
        # 1 part for the left column (file chooser), 2 parts for the right column (content display)
        col1, col2, col3 = st.columns([1, 0.05, 2])

        # In the left column (file selection dropdown)
        with col1:
            # Convert list of dictionaries into a single dictionary
            file_dict = {file['path']: file['content']
                         for file in st.session_state.repo_contents}

            # Only need to do it once, not each time the user selects a new file
            file_names = list(file_dict.keys())

            # Display the list of files
            selected_file = st.selectbox(
                "Browse the files", file_names)

            if selected_db:
                st.page_link("pages/choose_files.py",
                             label="Confirm Choice", icon="📂")

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
            # Stops at the first match for the selected file
            file_content = file_dict.get(selected_file, "File not found")
            if file_content:
                # Display file content inside a larger white box
                st.markdown(
                    f"""
                    <div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px;
                                border: 1px solid #ccc; height: 400px; overflow-y: auto;
                                color: black; white-space: pre-wrap; display: flex; align-items: flex-start;">
                        <pre style="color: black; margin: 0; padding: 0; line-height: 1.2;">{file_content.lstrip()}</pre>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
