import streamlit as st
import pandas as pd
from github_connector import connector_github
from code_editor import code_editor

#################################################################################
###################### SESSION_STATE ############################################
#################################################################################

# Clears all stored values
st.session_state.clear()

# Save the library object - will be used across the pages
# Also resets the object
st.session_state.object = connector_github()

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
    st.logo(
        "https://closer.pt/wp-content/uploads/2024/03/Closer_white.svg")
    st.header("Navigation")
    st.page_link("homepage.py", label="Home", icon="🏠", disabled=True)

cols1, cols2 = st.columns([1, 1])
with cols1:
    st.image(
        "https://closer.pt/wp-content/uploads/2024/03/Closer_white.svg", width=250)
# Format both the start and end dates by taking the first 10 characters

############################################################################################
################################# CODE #####################################################
############################################################################################

# Spacer between logo and metrics
st.write("")

# Debugging
# st.write(f"{st.session_state.object.current_env()}")

with st.popover("GitHub", use_container_width=True):
    token = st.text_input("Please insert your token:")

# Define the error message
error_message = "⚠️ Invalid Token ⚠️"

if len(token) > 0:
    try:
        st.session_state.object.authenticate(token)
        st.switch_page("pages/choose_new_repos.py")
    except Exception:
        st.warning(error_message)
        st.stop()

# Spacer
st.write("")

if st.button("Local Upload (Without Github)", use_container_width=True):
    st.switch_page("pages/no_github_approach.py")


# if "initial_code" not in st.session_state:
#     st.session_state.initial_code = "print('Hello, world!')"
#
# list = [1]
#
# button_save = [{
#     "name": "Save changes",
#     "feather": "Save",
#     "primary": "true",
#     "hasText": "true",
#     "showWithIcon": "true",
#     "commands": ["submit"],
#     "alwaysOn": True,
#     "style": {
#             "bottom": "0.40rem",
#             "right": "0.3rem"
#     }
# }]
#
# # Store editor content in session state
# if 'editor_content' not in st.session_state:
#     st.session_state.editor_content = st.session_state.initial_code
#
# updated_code = code_editor(st.session_state.editor_content, lang="python",
#                            theme="dark", buttons=button_save)
#
# # Only update when save button is pressed
# if updated_code['type'] == 'submit':
#     st.session_state.editor_content = updated_code['text']
#     if updated_code['text'] != st.session_state.initial_code:
#         list[-1] = updated_code['text']
#         st.write("The code has been modified!")
#         st.write(updated_code['text'])
#         st.write(f"This is {list}")
#     else:
#         st.write("No changes detected.")
#         st.write(updated_code['text'])
#         st.write(f"This is {list}")
