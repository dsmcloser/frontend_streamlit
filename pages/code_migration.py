import streamlit as st
import pandas as pd
from github_connector import connector_github
import time

###############################################################################
###################### SESSION_STATE ##########################################
###############################################################################

# Triggers if the session state is lost, basically whenever you reload the page
if "object" not in st.session_state:
    st.warning("You need to log in again. Redirecting...")
    time.sleep(2)
    st.switch_page("homepage.py")

# Make sure the button is initially disabled
st.session_state.button_disabled = True

# Make sure that the branch is reset to default incase user goes back
# from the final comparison page
st.session_state.object.current_branch = None

# Only fetches the branches once
st.session_state.branch_list = st.session_state.object.get_all_branches()

# If there are less selected files than the number of files, then
# the new branch must be emptied and then filled with the selected files
if st.session_state.file_nr != len(st.session_state.selected_files):
    st.session_state.create_specific_branch = True
else:
    st.session_state.create_specific_branch = False

if 'branch_was_created' not in st.session_state:
    st.session_state.branch_was_created = False
#################################################################################
#################################################################################
#################################################################################


# Set up page configuration and load CSS styles
st.set_page_config(
    page_title="Branch Creation",
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
    st.switch_page("pages/choose_files.py")

if st.button("🔄"):
    st.rerun()

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

st.title("Code Migration")

# Branch creation
st.markdown("<h1 style='text-align: center;'>Create a branch</h1>",
            unsafe_allow_html=True)
branch_name = st.text_input("Enter a name for the new branch:")

# Check if the branch name is valid
if branch_name in st.session_state.branch_list:
    st.warning("Branch already exists")
    st.session_state.button_disabled = True

else:
    if len(branch_name) > 0:
        st.success("The name is valid, you may proceed")
        st.session_state.button_disabled = False

# Dropdown for scenario selection
scenario = st.selectbox("Choose the type of migration:", [
                        "DOTNET/JAVA", "PYTHON"], disabled=st.session_state.button_disabled)

# Dropdown for approach selection
processing_type = st.selectbox("Type of processing:", [
    'Auto', 'Manual'], disabled=st.session_state.button_disabled)

# Lets user know that the branch is being created after clicking the button
with st.spinner("Building the new branch...", show_time=True):

    # Create branch
    if st.button("Continue", disabled=st.session_state.button_disabled):
        if st.session_state.create_specific_branch:
            try:
                st.session_state.object.create_branches_from_main(branch_name)
                st.session_state.object.clear_branch()

                st.session_state.object.upload_file(
                    st.session_state.repo_contents,
                    st.session_state.selected_files)

                # st.session_state.object.switch_to_branch("main")
                st.session_state.new_branch = branch_name

                # time.sleep(30)
                st.session_state.branch_was_created = True

                if scenario == 'DOTNET/JAVA' and processing_type == 'Manual':
                    # st.switch_page("pages/dotnet_java.py")
                    st.switch_page("pages/dotnet_java.py")
                else:
                    # st.switch_page("pages/python.py")
                    st.switch_page("pages/dotnet_java_auto.py")

            except Exception as e:
                error_message = str(e)
                st.warning(f"⚠️ {error_message}")

        else:
            try:
                st.session_state.object.create_branches_from_main(branch_name)
                st.session_state.new_branch = branch_name
                # time.sleep(30)
                st.session_state.branch_was_created = True

                # Redirect to the next page
                st.write(f"Redirecting to the next page {scenario}")

                if scenario == 'DOTNET/JAVA' and processing_type == 'Manual':
                    # st.switch_page("pages/dotnet_java.py")
                    st.switch_page("pages/dotnet_java.py")
                else:
                    # st.switch_page("pages/python.py")
                    st.switch_page("pages/dotnet_java_auto.py")

            except Exception as e:
                error_message = str(e)
                st.warning(f"⚠️ {error_message}")

# if st.button('Dotnet page'):
#     st.switch_page("pages/dotnet_java.py")
# If the branch is created and the button was pressed
# if st.session_state.branch_was_created and st.button("Keep the same branch"):
#
#    # Redirect to the next page
#    if scenario == 'DOTNET/JAVA':
#        st.switch_page("pages/dotnet_java.py")
#    else:
#        st.switch_page("pages/python.py")

# Debugging
# st.write(st.session_state.object.current_env())

# if st.button("MOVE ON FOR TESTING!!!"):
#     st.switch_page("pages/final_comparison.py")
