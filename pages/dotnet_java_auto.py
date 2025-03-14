import logging
import streamlit as st
import pandas as pd
from github_connector import connector_github
import time
from backend_access import handle_request_sync, ENDPOINTS

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
# st.session_state.object.current_branch = None

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

# Store the files to uploaded (the migrated version)
if 'to_upload' not in st.session_state:
    st.session_state.to_upload = []

# Usefull to iterate over the selected files
if 'current_file' not in st.session_state:
    st.session_state.current_file = 0

if 'progress_display' not in st.session_state:
    st.session_state.progress_display = []

#################################################################################
#################################################################################
#################################################################################


# Set up page configuration and load CSS styles
st.set_page_config(
    page_title="Automatic Code Processing",
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
#     st.switch_page("pages/code_migration.py")

if st.button("🔄"):
    st.rerun()

#################################################################################
#################################################################################
#################################################################################

# Debugging
# st.write(f"{st.session_state.object.current_env()}")


###############################################################################
# def create_sidebar(curr_page):
#    with st.sidebar:
#        st.logo(
#            "https://closer.pt/wp-content/uploads/2024/03/Closer_white.svg")
#        st.header("Pages")
#        st.page_link("homepage.py", label="Home", icon="🏠",
#                     disabled=(curr_page == "homepage"))
#        st.page_link("pages/dotnet_java.py", label="SPMS code migration",
#                     icon="1️⃣", disabled=(curr_page == "spms_frontend"))
#        # st.page_link("pages/show_jobs.py", label="Shows all jobs",
#        #             icon="2️⃣", disabled=(curr_page == "show_jobs"))


# create_sidebar("spms_frontend")

if "testing" not in st.session_state:
    st.session_state["testing"] = False

if "file_name" not in st.session_state:
    st.session_state["file_name"] = ""

result = ""
code = ""
job_id = ""

net_version = ""
java_version = ""

# List of .NET versions
net_options = [".NET 1.0", ".NET 1.1", ".NET 2.0", ".NET  3.0", ".NET 3.5",
               ".NET 4", ".NET 4.5", ".NET 4.5.1", ".NET 4.5.2", ".NET 4.6",
               ".NET 4.6.1", ".NET 4.6.2", ".NET 4.7", ".NET 4.7.1",
               ".NET 4.7.2", ".NET 4.8", ".NET 4.8.1"]

# List of Java versions
java_options = ["Java 8", "Java 11", "Java 17 (Recommended)",
                "Java 21 (Recommended)", "Java 23 (Newest)"]

# Default index for Java 17
java_index = java_options.index("Java 17 (Recommended)")
st.session_state["java_index"] = java_index

logo_url = "https://closer.pt/wp-content/uploads/2024/03/Closer_white.svg"

st.image(logo_url, width=250)


def clean_java_block(java_block):
    """
    Removes ```java at the start of the string and ``` at the end of the string.
    It is used because the llm response has that blocks on it.
    """
    return java_block.replace("```java", "").replace("```", "").strip()


# Menu configuration for API calls.
with st.container(border=True):
    col1, col2, col3 = st.columns(3)
    with col1:
        use_ast = st.checkbox("Use AST", value=False, key="use_ast")
        st.checkbox("Check comments", value=True, key="check_comments")
    with col2:
        st.checkbox("Check datatype", value=True, key="check_datatype")
        st.checkbox("Check functionality", value=True,
                    key="check_functionality")
    with col3:
        st.checkbox("Check libraries", value=True, key="check_libraries")
        st.checkbox("Check syntax", value=True, key="check_syntax")

with st.container(border=True):
    col1, col2, col3, col4 = st.columns([2, 1, 2, 2])

    # Select the versions of the languages
    with col1:
        net_version = st.selectbox(
            "Select .NET version",
            net_options
        )
        java_version = st.selectbox(
            "Select Java version LTS",
            java_options,
            index=java_index
        )

    ################################################################################
    ################################################################################
    ################################################################################

    # Calls the API to migrate the code and give the result back
    with col3:
        button = st.button("Migrate code")
        if button:
            limit = len(st.session_state.selected_files)

            # Setup the progress bar
            total_steps = limit
            status_text = st.empty()  # Placeholder for dynamic updates

            with st.spinner("Processing...", show_time=True):
                while st.session_state.current_file < limit:
                    # Update the progress bar
                    for step in range(1, total_steps + 1):
                        uploaded_file = st.session_state.selected_files[st.session_state.current_file]

                        status_text.markdown(
                            f"**Processing {uploaded_file['path']}...**<br>"
                            f"Step {step} of {total_steps}...", unsafe_allow_html=True)  # Use <br> for line break and enable HTML

                        if uploaded_file is not None:
                            st.session_state["file_name"] = uploaded_file['path']
                            # bytes_data = uploaded_file['content']
                            code = uploaded_file['content']

                        result = handle_request_sync(
                            ENDPOINTS["CODE_MIGRATION_NET_JAVA"],
                            code=code,
                            net_version=net_version,
                            java_version=java_version, use_ast=use_ast
                        )

                        # If the migration fails, the clean_java_block would
                        # get an error because the result is empty
                        if not result:
                            st.warning(
                                'Something went wrong with the migration!')

                        else:
                            result = clean_java_block(java_block=result)
                            # result = "using System; using System.IO; public class ConstrainedGenericClass<T> where T : new() { static void Main() { string f='example.txt'; File.WriteAllText(f,'Hello, World!'); Console.WriteLine('File Content: ' + File.ReadAllText(f)); File.AppendAllText(f, '\nAppended Text'); Console.WriteLine('Updated File Content: ' + File.ReadAllText(f)); } }"
                            st.session_state["result"] = result
                            st.session_state["code"] = code
                            st.session_state["net_version"] = net_version
                            st.session_state["java_version"] = java_version
                            st.session_state["testing"] = False

                            file_name = st.session_state.selected_files[st.session_state.current_file]
                            # Add the new content to the same file
                            st.session_state.to_upload.append(
                                {'path': file_name['path'], 'content': result})

                            st.session_state.progress_display.append(
                                file_name['path'])

                            st.session_state.current_file += 1

                            # Resets all the workflow when migrating code again
                            if "job_id" in st.session_state:
                                del st.session_state["job_id"]
                            if "current_step" in st.session_state:
                                del st.session_state["current_step"]
                            if "step_results" in st.session_state:
                                del st.session_state["step_results"]
                            if "status_res" in st.session_state:
                                del st.session_state["status_res"]

                status_text.markdown(
                    "✅ **Migration complete!**")

                status_text.markdown('**Uploading the results...**')
                # When the loop is done, upload all files at once
                st.session_state.object.upload_file(
                    st.session_state.repo_contents,
                    st.session_state.to_upload)

                st.switch_page("pages/final_comparison.py")

# Shows the result of the code migration compared to the code
# if "result" in st.session_state:
#     result = st.session_state["result"]
#     code = st.session_state["code"]
#     with st.container(border=True):
#         with st.expander("Result"):
#             cols1, cols2 = st.columns(2)
#
#             with cols1:
#                 if code:
#                     st.write("Code Deployed")
#                     st.code(code, language="csharp")
#
#             with cols2:
#                 if result:
#                     st.write("Code Migrated")
#                     st.code(result, language="java")


# Button to start testing, receives job_id to follow job work
if result and not st.session_state["testing"]:
    test_result_btn = st.button("Test Result")
    if test_result_btn:
        with st.spinner("Processing..."):
            # job_id = handle_request_sync(
            #     ENDPOINTS["NET_JAVA_TESTS"],
            #     code_migrated=result,
            #     source_code=code,
            #     net_version=net_version,
            #     java_version=java_version,
            #     file_name=st.session_state["file_name"],
            #     check_comments=st.session_state["check_comments"],
            #     check_datatype=st.session_state["check_datatype"],
            #     check_functionality=st.session_state["check_functionality"],
            #     check_libraries=st.session_state["check_libraries"],
            #     check_syntax=st.session_state["check_syntax"]
            # )
            job_id = "e5a07659-a31d-4ca9-b4fa-19b947a1691a"
            st.session_state["job_id"] = job_id
            st.session_state["testing"] = True
            # st.switch_page("pages/show_jobs.py")
            st.warning("AQUI É SUPOSTO MUDAR DE PÁGINA")


if "status_res" in st.session_state:
    st.code(st.session_state["status_res"])
