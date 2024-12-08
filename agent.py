import logging
import importlib
import os
import sys
from toolbox.tools import BaseTool
from config import AgentConfig
from api_client import GroqAPI  # Updated to GroqAPI


# Base Agent
class BaseAgent:
    def __init__(self, config: AgentConfig):
        """
        Initializes the BaseAgent with configuration, tools, and state management.
        """
        self.config = config
        self.tools = {}
        self.state = {}
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
        )
        self.logger = logging.getLogger(self.__class__.__name__)

    def register_tool(self, tool: BaseTool):
        """
        Registers a tool for the agent.
        """
        self.tools[tool.name()] = tool
        self.logger.info(f"Tool '{tool.name()}' registered successfully.")


# Main Agent
class Agent(BaseAgent):
    def __init__(self, config: AgentConfig):
        super().__init__(config)
        self.api_client = GroqAPI(config)  # Updated to use GroqAPI

        # Automatically register tools from the toolbox directory
        self.auto_register_tools()

        # Build system prompt
        tool_descriptions = "\n".join(
            f"- {tool.name()}: {tool.description()}" for tool in self.tools.values()
        )
        self.system_prompt = f"""You are {config.role}.
Available tools:
{tool_descriptions}

RULES:
1. Output ONLY executable Python code.
2. Your answer MUST start with 'Answer:' and end with '###'.
3. NO explanations or comments.
4. Use the registered tools dynamically."""

    def auto_register_tools(self):
        """
        Automatically registers all tools from the toolbox directory.
        """
        sys.path.append(os.path.abspath(os.path.dirname(__file__)))

        toolbox_dir = os.path.join(os.path.dirname(__file__), "toolbox")
        for root, _, files in os.walk(toolbox_dir):
            for file in files:
                if file.endswith(".py") and file != "__init__.py":
                    module_path = os.path.relpath(os.path.join(root, file), start=os.path.dirname(__file__))
                    module_name = module_path.replace(os.sep, ".").rsplit(".", 1)[0]
                    try:
                        self.logger.info(f"Attempting to load module: {module_name}")
                        module = importlib.import_module(module_name)
                        for attr in dir(module):
                            obj = getattr(module, attr)
                            if isinstance(obj, type) and issubclass(obj, BaseTool) and obj is not BaseTool:
                                tool_instance = obj(self.state) if "state" in obj.__init__.__code__.co_varnames else obj()
                                self.register_tool(tool_instance)
                    except Exception as e:
                        self.logger.error(f"Failed to load tool from module '{module_name}': {e}")

    def run(self, task_description: str) -> str:
        """
        Executes a task using a matching tool or default logic.
        :param task_description: The description of the task to execute.
        :return: The result of the task execution.
        """
        try:
            # Identify the relevant tool based on task content
            for tool_name, tool in self.tools.items():
                if tool_name in task_description.lower():
                    self.logger.info(f"Using tool '{tool_name}' to execute task: {task_description}")
                    result = tool.execute(task_description)
                    self.state[f"last_{tool_name}_result"] = result
                    return result

            # Default fallback
            raise ValueError("No matching tool found for the task description.")

        except Exception as e:
            self.logger.error(f"Failed to execute task: {e}")
            return f"Error during execution: {e}"
