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

#################################################################################
########################## SIDEBAR AND LOGO #####################################
#################################################################################

# Set up page configuration and load CSS styles
st.set_page_config(
    page_title="File Selection",
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
    if not st.session_state.local_upload:
        st.switch_page("pages/repositories.py")
    else:
        st.switch_page("pages/local_upload.py")

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

# Debugging
# st.write(f"{st.session_state.object.current_env()}")

st.title(f"Choose files from {st.session_state.object.current_repo.name}")

# Create Layout (Three Columns: Selector | Divider | Preview)
col1, col2, col3 = st.columns([1, 0.05, 2])  # Adjust widths as needed

with col1:
    st.header("📂 Select Files")

    options = [file["path"] for file in st.session_state.repo_contents]

    # Create DataFrame from file list
    df = pd.DataFrame({"File Name": [file["path"]
                                     for file in st.session_state.repo_contents]})

    # Column Configuration for Styling
    column_configuration = {
        "File Name": st.column_config.TextColumn(
            "Files Available", help="Select the files you want to process", width="medium"
        )
    }

    # Display files with selection enabled
    event = st.dataframe(
        df,
        column_config=column_configuration,
        use_container_width=True,
        hide_index=True,
        on_select="rerun",
        selection_mode="multi-row",
    )

    # Get selected rows
    selected_rows = event.selection.rows
    selected_files = df.iloc[selected_rows]["File Name"].tolist()

    selections = event.selection
    number_of_selected_files = len(selections['rows'])

    if number_of_selected_files == len(options):
        st.write(f"All files are selected ({number_of_selected_files})")
    elif number_of_selected_files == 0:
        st.write(f"No files are selected ({number_of_selected_files})")
    else:
        st.write(f"Some files are selected ({number_of_selected_files})")


with col2:
    # Vertical divider
    st.markdown(
        """
        <div style="height: 60vh; border-left: 2px solid #ccc; margin: auto;"></div>
        """,
        unsafe_allow_html=True
    )

with col3:
    # Display selected file contents
    st.markdown("### File Preview (last 5 selections)")

    if selected_files:
        # Limit the number of files to display in the frontend
        shortlist = selected_files[:5]
        for selected_file in shortlist:
            file_data = next(
                (file for file in st.session_state.repo_contents if file["path"] == selected_file), None)
            if file_data:
                st.markdown(f"**{selected_file} preview:**")
                st.code(file_data["content"][:30] +
                        ' ...', language="plaintext")

        # Allows for the selection of all files in the next couple of pages
        st.session_state.selected_files = []
        for selected_file in selected_files:
            file_data = next(
                (file for file in st.session_state.repo_contents if file["path"] == selected_file), None)
            if file_data:
                st.session_state.selected_files.append(file_data)
    else:
        st.markdown("_Select a file to see its content._")

if len(selected_files) > 0:
    st.session_state.file_nr = len(df)
    st.page_link("pages/code_migration.py",
                 label="Upload these files", icon="⬆️")
