from .base import init_model
from langchain.agents import create_agent
from datetime import datetime
import json
import logging
from langchain.agents.middleware import TodoListMiddleware, ToolRetryMiddleware
from tools.tools import pentest_shell, shell_documentation
from deepagents import CompiledSubAgent

# fetch tool header from config
available_tools = json.load(open("./config.json", "r"))['tools']['reconnaissance']
general_tools = json.load(open("./config.json", "r"))['tools']['general']
available_tools.extend(general_tools)
available_tools.extend([shell_documentation])

today = datetime.now().strftime("%Y-%m-%d")

# setup logging
logger = logging.getLogger('recon_agent')
logger.setLevel(logging.INFO)

instrctions = """
You are a reconnaissance agent. Your goal is to gather as much information as possible about the target system or network using the available tools. 
Use the tools effectively to perform tasks such as DNS enumeration, subdomain discovery, WHOIS lookups, and other reconnaissance activities.
Be thorough in your information gathering and document your findings clearly.
Follow these guidelines:
1. Start with basic information gathering using WHOIS and DNS tools.
2. Use subdomain discovery tools to identify potential targets.
3. Analyze the gathered data to identify patterns or potential vulnerabilities.
4. Always document your findings with timestamps for future reference.
5. Prioritize stealth and avoid detection while performing reconnaissance tasks.
6. If you encounter any issues or need additional information, adjust your approach accordingly.
Remember, the quality of your reconnaissance will significantly impact the success of subsequent penetration testing phases.
Use the following tools as needed: {available_tools}
Use the shell documentation tool to search for pentest tools usage and examples. 
Make sure to log the date and time of each action you take. today is {today}.
"""

class ReconAgent:
    def __init__(self):

        # initialize model
        model = init_model().get_model()

        self.agent = create_agent(
            model=model,
            tools=[pentest_shell, shell_documentation],  # Define or import recon tools as needed
            system_prompt=instrctions.format(available_tools=available_tools, today=today),
            name='recon_agent',
            middleware=[
                TodoListMiddleware(),
                ToolRetryMiddleware(
                    max_retries=3,
                    on_failure="continue"
                )
            ],

        )

        logger.info("Recon Agent initialized.")

    def get_agent(self):
        return self.agent
    
    def get_compiled_agent(self) -> CompiledSubAgent:

        compiled_agent = CompiledSubAgent(
            name="recon_agent",
            description="A reconnaissance agent for gathering information about target systems and networks.",
            runnable=self.agent,
        )

        return compiled_agent
    