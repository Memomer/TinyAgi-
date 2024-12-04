import logging
from tools import BaseTool, Calculator, NoteTaker
from config import AgentConfig
from api_client import HuggingFaceAPI


# Base Agent
class BaseAgent:
    def __init__(self, config: AgentConfig):
        """
        Initializes the BaseAgent with configuration, tools, and state management.
        """
        self.config = config
        self.tools = {}
        self.state = {}

    def register_tool(self, tool: BaseTool):
        """
        Registers a tool for the agent.
        """
        self.tools[tool.name()] = tool
        logging.info(f"Tool '{tool.name()}' registered successfully.")


# Main Agent
class Agent(BaseAgent):
    def __init__(self, config: AgentConfig):
        super().__init__(config)
        self.api_client = HuggingFaceAPI(config)

        # Initialize and register tools
        self.register_tool(Calculator())
        self.register_tool(NoteTaker(self.state))

        # Build system prompt
        tool_descriptions = "\n".join(
            f"- {tool.name()}: {tool.description()}"
            for tool in self.tools.values()
        )
        self.system_prompt = f"""You are {config.role}.
Available tools:
{tool_descriptions}

RULES:
1. Output ONLY executable Python code.
2. Your answer MUST start with 'Answer:' and end with '###'.
3. NO explanations or comments.
4. NO markdown formatting.
5. Use ONLY these patterns:
   - result = calculate("expression")
   - save_note("label", value)
   - save_note("content")"""

    def run(self, user_input: str) -> str:
        """
        Executes a task by generating Python code, validating it, and executing it.
        """
        try:
            # Generate the prompt
            prompt = f"""<s>[INST] {self.system_prompt}

Task: {user_input}
Generate Python code to solve this task using the available tools. [/INST]"""

            # Get raw output from the API
            raw_output = self.api_client.generate_response(prompt)
            logging.info(f"Generated raw output:\n{raw_output}")

            # Extract and clean the generated code
            code = self._extract_code(raw_output)
            logging.info(f"Extracted and cleaned code:\n{code}")

            # Validate the extracted code
            self._validate_code(code)

            # Execute the validated code
            local_dict = {tool.name(): tool.execute for tool in self.tools.values()}
            exec(code, {}, local_dict)

            # Update the state with results
            self._update_state()

            return str(self.state)

        except Exception as e:
            logging.error(f"Agent execution failed: {str(e)}")
            return f"Error during execution: {str(e)}"

    def _extract_code(self, raw_output: str) -> str:
        """
        Extracts the Python code between 'Answer:' and '###'.
        """
        try:
            start_marker = "Answer:"
            end_marker = "###"

            start_index = raw_output.find(start_marker)
            end_index = raw_output.find(end_marker, start_index)

            if start_index == -1 or end_index == -1:
                raise ValueError("Code boundaries ('Answer:' and '###') not found in the output.")

            # Extract and clean the code
            code = raw_output[start_index + len(start_marker):end_index].strip()

            if not code:
                raise ValueError("Extracted code is empty or invalid.")

            return code

        except Exception as e:
            logging.error(f"Code extraction failed: {str(e)}")
            raise

    def _validate_code(self, code: str):
        """
        Validates the extracted code to ensure it uses only allowed patterns and avoids unsafe operations.
        """
        allowed_patterns = ["calculate(", "save_note("]
        prohibited_keywords = ["exec", "eval", "__", "import"]

        # Ensure allowed patterns are used
        if not any(pattern in code for pattern in allowed_patterns):
            raise ValueError("Generated code does not use any of the allowed tools.")

        # Check for prohibited keywords
        if any(keyword in code for keyword in prohibited_keywords):
            raise ValueError("Generated code contains prohibited or unsafe operations.")

    def _update_state(self):
        """
        Updates the agent's state with the last result from each tool.
        """
        for name, tool in self.tools.items():
            if hasattr(tool.execute, 'last_result'):
                self.state[f'last_{name}_result'] = tool.execute.last_result
