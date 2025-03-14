import streamlit as st
import logging
from telemetry import configure_logger
from elements.sidebar import create_sidebar
# from backend_access import handle_request_sync
# from backend_access import ENDPOINTS


st.set_page_config(
    page_title="SPMS code migration",
    page_icon=(
        "https://closer.pt/wp-content/uploads/2024/04/For_ico-150x150.png"
    ),
    layout="wide"  # Ensures the layout spans the full width
)


with open('.streamlit/style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

configure_logger()
logger = logging.getLogger("GenAIlog")

create_sidebar("spms_frontend")

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
    col1, col2, col3 = st.columns([2, 1, 1])
    # File uploader and reset to the workflow in case it was done before
    with col1:
        uploaded_file = st.file_uploader(
            "Choose a file")
        st.code(uploaded_file)
        if uploaded_file is not None:
            st.session_state["file_name"] = uploaded_file.name
            bytes_data = uploaded_file.getvalue()
            code = bytes_data.decode("windows-1252")

    # Select the versions of the languages
    with col3:
        if code:
            net_version = st.selectbox(
                "Select .NET version",
                net_options
            )
            java_version = st.selectbox(
                "Select Java version LTS",
                java_options,
                index=java_index
            )

    # Calls the API to migrate the code and give the result back
    with col2:
        if code:
            button = st.button("Migrate code")
            if button:
                with st.spinner("Processing..."):
                    # result = handle_request_sync(
                    #     ENDPOINTS["CODE_MIGRATION_NET_JAVA"],
                    #     code=code,
                    #     net_version=net_version,
                    #     java_version=java_version, use_ast=use_ast
                    # )
                    # result = clean_java_block(java_block=result)
                    result = "using System; using System.IO; public class ConstrainedGenericClass<T> where T : new() { static void Main() { string f='example.txt'; File.WriteAllText(f,'Hello, World!'); Console.WriteLine('File Content: ' + File.ReadAllText(f)); File.AppendAllText(f, '\nAppended Text'); Console.WriteLine('Updated File Content: ' + File.ReadAllText(f)); } }"
                    st.session_state["result"] = result
                    st.session_state["code"] = code
                    st.session_state["net_version"] = net_version
                    st.session_state["java_version"] = java_version
                    st.session_state["testing"] = False
                # Resets all the workflow when migrating code again
                if "job_id" in st.session_state:
                    del st.session_state["job_id"]
                if "current_step" in st.session_state:
                    del st.session_state["current_step"]
                if "step_results" in st.session_state:
                    del st.session_state["step_results"]
                if "status_res" in st.session_state:
                    del st.session_state["status_res"]

# Shows the result of the code migration compared to the code
if "result" in st.session_state:
    result = st.session_state["result"]
    code = st.session_state["code"]
    with st.container(border=True):
        with st.expander("Result"):
            cols1, cols2 = st.columns(2)

            with cols1:
                if code:
                    st.write("Code Deployed")
                    st.code(code, language="csharp")

            with cols2:
                if result:
                    st.write("Code Migrated")
                    st.code(result, language="java")


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

st.json(st.session_state)
