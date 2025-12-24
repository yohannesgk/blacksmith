from langchain.tools import tool
import requests
import os
from langgraph.config import get_stream_writer
import json
from langchain_mcp_adapters.client import MultiServerMCPClient
import asyncio
from utils.vectors import storage_manager
from agents.base import init_embedding_model

config_tools = json.load(open("./config.json", "r"))['tools']
code_interpreter_config = json.load(open("./mcp/mcp-code-interpreter.json", "r"))['mcpServers']
playwright_config = json.load(open("./mcp/mcp-playwright.json", "r"))['mcpServers']
mcp_full = json.load(open("./mcp/mcp.json", "r"))['mcpServers']
sleep = 2


@tool
def pentest_shell(command: str, timeout: int = 300):
    """
    This tool run a shell commands for pentesting.
    As of now these tools are available besides basic linux commands:

        "reconnaissance": [
            "whois", "dnsutils (dig/nslookup)", "dnsrecon",
            "assetfinder", "findomain", "subfinder"
        ],
        "scanning_enumeration": [
            "nmap", "masscan", "enum4linux-ng",
            "gobuster", "wpscan", "fingerprintx"
        ],
        "vulnerability_mapping": [
            "nuclei", "sslscan"
        ],
        "exploitation": [
            "sqlmap", "hydra", "medusa", "ncrack"
        ],
        "post_exploitation": [
            "netcat-traditional", "socat", "hping3",
            "impacket CLIs (psexec, smbclient, secretsdump)"
        ],
        "general": [
            "python3", "pip3", "Go toolchain (go install tools)", 
            "build-essential", "gcc", "gdb", "strace",
            "flask", "httpie", "curl", "openssh-client"
        ]
    
    Args:
        command: bash command e.g nmap -sV -p 80,21 10.10.1.173
        timeout: command execution timeout in seconds (default: 300 seconds)
    """

    # initialize custom stream writer
    writer = get_stream_writer()
    writer(f"running command {command}")

    response = requests.post(
        os.getenv('container_uri', 'http://localhost:9756/exec'),
        json={"cmd": command, "timeout": timeout}
    )

    if response.status_code != 200:
        writer(f"command execution failed with status code {response.status_code}")
        return f"Error: Command execution failed with status code {response.status_code}"
    
    writer("command executed, processing response...")

    return response.json()

# initialize vector store for tool documentation
embedding_model = init_embedding_model().get_model()

shell_documentation_vector_store = storage_manager(
        collection_name="tools_documentation",
        persist_directory="./store/vector_db",
        embedding_function=embedding_model
    )

# tool for shell command documentation
@tool
def shell_documentation(query: str):
    """
    This tools provides documentation for the pentest shell commands available in the pentest shell tool.

    Args:
        query: The documentation query string.
    Returns:
        A string containing relevant documentation snippets related to the query.
    """
    # initialize custom stream writer
    writer = get_stream_writer()
    writer(f"searching documentation for query: {query}")
    results = shell_documentation_vector_store.query(query, n_results=5)
    writer(f"found {len(results)} relevant documents.")
    docs_content = "\n\n".join([doc.page_content for doc in results])
    return f"Here are some relevant documentation snippets:\n\n{docs_content}"

#####################################################################################
# MCP Tools
#####################################################################################

async def browser():
    """
    Returns MCP Playwright browser tools with responses wrapped to extract text content.
    This ensures tool responses are plain strings compatible with all LLM providers.
    """
    mcp_data = MultiServerMCPClient(playwright_config)
    tools = await mcp_data.get_tools()
    await asyncio.sleep(sleep)
    
    return tools

async def code_executor():
    
    mcp_data = MultiServerMCPClient(code_interpreter_config)
    tools = await mcp_data.get_tools()
    await asyncio.sleep(sleep)
    
    return tools
