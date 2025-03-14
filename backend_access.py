import aiohttp
import asyncio
import os
import logging


logger = logging.getLogger("GenAIlog")

ENDPOINTS = {
    "CODE_MIGRATION_AZURE": "complete/codemigration/azure",
    "VALIDATE_SQL": "validation/code/sql",
    "CODE_MIGRATION_NET_JAVA": "codemigration/net-java",
    "NET_JAVA_TESTS": "codemigration/net-java-tests",
    "NET_JAVA_JOBS": "codemigration/net-java-job/jobs",
    "NET_JAVA_JOB_STATUS": "codemigration/net-java-job/status",
    "CREATE_AST": "csharp/create-ast"
}

GET_APIS = [ENDPOINTS["NET_JAVA_JOBS"],
            ENDPOINTS["NET_JAVA_JOB_STATUS"]]

POST_APIS = [ENDPOINTS["CODE_MIGRATION_AZURE"], ENDPOINTS["VALIDATE_SQL"],
             ENDPOINTS["CODE_MIGRATION_NET_JAVA"], ENDPOINTS["NET_JAVA_TESTS"], ENDPOINTS["CREATE_AST"]]

ENDPOINTS_RESPONSES = {
    ENDPOINTS["CODE_MIGRATION_AZURE"]: "code-migration-azure",
    ENDPOINTS["VALIDATE_SQL"]: "sql_code",
    ENDPOINTS["CODE_MIGRATION_NET_JAVA"]: "code-migration-net-java",
    ENDPOINTS["NET_JAVA_TESTS"]: "code-migration-net-java-tests",
    ENDPOINTS["NET_JAVA_JOBS"]: "code-migration-net-java-jobs",
    ENDPOINTS["NET_JAVA_JOB_STATUS"]: "code-migration-net-java-job-status",
    ENDPOINTS["CREATE_AST"]: "csharp-ast"
}


async def async_send_request(endpoint, **kwargs):
    return await send_request(endpoint, **kwargs)


def handle_request_sync(endpoint, current_question=None, file_name=None,
                        code=None,  net_version=None, java_version=None,  code_migrated=None, source_code=None, job_id=None, use_ast=None,
                        check_comments=True, check_datatype=True, check_functionality=True, check_libraries=True, check_syntax=True):
    # Use asyncio.run() here if outside Streamlit's synchronous context
    # You cannot use asyncio.run() directly within Streamlit's reactive code
    result = asyncio.run(async_send_request(
        endpoint, current_question=current_question, file_name=file_name,
        code=code, net_version=net_version, java_version=java_version, code_migrated=code_migrated, source_code=source_code, job_id=job_id, use_ast=use_ast,
        check_comments=check_comments, check_datatype=check_datatype, check_functionality=check_functionality, check_libraries=check_libraries, check_syntax=check_syntax))

    return result


class HTTPERRORException(Exception):
    pass


async def handle_response(response, endpoint, retry):
    data = None
    if response.status == 200:
        data = await response.json()
        return data.get(ENDPOINTS_RESPONSES[endpoint])

    elif response.status == 429:
        logger.warning(f"Rate limit exceeded, retrying in"
                       f"{retry + 1} seconds...")
        # Exponential backoff
        await asyncio.sleep(retry + 1)
    else:
        logger.error(f"HTTP error {response.status}: {await response.text()}")
        raise HTTPERRORException
    return data


async def send_request(endpoint, current_question=None, max_retries=2, file_name=None,
                       code=None, net_version=None, java_version=None, code_migrated=None, source_code=None,  job_id=None, use_ast=None,
                       check_comments=None, check_datatype=None, check_functionality=None, check_libraries=None, check_syntax=None):
    url = "https://spms-backend-gdcwcagpgqe7e6du.westeurope-01.azurewebsites.net"
    api_key = "Z-k!4g+$bwW}%U=[0u_QfBkR-3D+Vu#+[17d{.vaYzf#.$##QSYz]ru99Cq1:3S31xFC8HiAXpPF:y-i"

    url_endpoint = f"{url}/{endpoint}/"
    headers = {
        'Authorization': f'{api_key}',
        'Content-Type': 'application/json',
    }

    payload = {}

    if endpoint == ENDPOINTS["CODE_MIGRATION_AZURE"] or endpoint == ENDPOINTS["VALIDATE_SQL"]:
        payload = {
            "code": current_question
        }
    elif endpoint == ENDPOINTS["CODE_MIGRATION_NET_JAVA"]:
        payload = {
            "code": code,
            "net_version": net_version,
            "java_version": java_version,
            "use_ast": use_ast
        }
    elif endpoint == ENDPOINTS["NET_JAVA_TESTS"]:
        payload = {
            "code_migrated": code_migrated,
            "source_code": source_code,
            "use_ast": use_ast,
            "net_version": net_version,
            "java_version": java_version,
            "file_name": file_name,
            "check_comments": check_comments,
            "check_datatype": check_datatype,
            "check_functionality": check_functionality,
            "check_libraries": check_libraries,
            "check_syntax": check_syntax
        }
    elif endpoint == ENDPOINTS["NET_JAVA_JOB_STATUS"]:
        url_endpoint = url_endpoint + f"{job_id}"
    elif endpoint == ENDPOINTS["CREATE_AST"]:
        payload = {
            "source_code": code
        }

    logging.info(f"Sending request to:\t{url_endpoint} with headers={headers}")
    async with aiohttp.ClientSession() as session:
        for retry in range(max_retries):
            try:
                if endpoint in GET_APIS:
                    async with session.get(url_endpoint, headers=headers) as response:
                        try:
                            data = await handle_response(
                                response, endpoint, retry)
                            if data:
                                return data
                        except HTTPERRORException:
                            break
                elif endpoint in POST_APIS:
                    async with session.post(url_endpoint, headers=headers, json=payload) as response:
                        try:
                            data = await handle_response(
                                response, endpoint, retry)
                            if data:
                                return data
                        except HTTPERRORException:
                            break
                else:
                    logging.error(f"The endpoint = '{endpoint}' is not valid!")
                    return None

            except aiohttp.ClientError as e:
                logger.error(f"Request failed: {e}")
                # Retry after delay in case of request failure
                await asyncio.sleep(retry + 1)

        logger.error(
            f"Failed to retrieve information after {max_retries} retries")
        return None
