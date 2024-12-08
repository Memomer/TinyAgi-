from abc import ABC, abstractmethod
from typing import Any, Dict

# Base Tool
class BaseTool(ABC):
    def __init__(self):
        self.last_result = None  # Instance-level attribute to store the last result

    @abstractmethod
    def name(self) -> str:
        """
        Returns the name of the tool.
        """
        pass

    @abstractmethod
    def description(self) -> str:
        """
        Returns a description of the tool's functionality.
        """
        pass

    @abstractmethod
    def execute(self, *args, **kwargs) -> Any:
        """
        Executes the tool's main functionality with the given arguments.
        """
        pass


# Calculator Tool
class Calculator(BaseTool):
    def name(self) -> str:
        return "calculate"

    def description(self) -> str:
        return "Performs mathematical calculations"

    def execute(self, expression: str) -> float:
        """
        Evaluates a mathematical expression.
        """
        try:
            # Safely evaluate the mathematical expression
            result = eval(expression, {"__builtins__": {}}, {})
            self.last_result = result  # Update the last_result attribute
            return result
        except Exception as e:
            raise ValueError(f"Invalid calculation: {str(e)}")


# Note Taker Tool
class NoteTaker(BaseTool):
    def __init__(self, state: Dict):
        super().__init__()  # Initialize BaseTool
        self.state = state
        self.notes = []

    def name(self) -> str:
        return "save_note"

    def description(self) -> str:
        return "Saves notes or results"

    def execute(self, content: str, label: str = None) -> str:
        """
        Saves a note with optional labeling.
        """
        # Construct the note object
        note = {"content": content, "label": label} if label else {"content": content}
        self.notes.append(note)  # Add the note to the internal notes list
        self.state["notes"] = self.notes  # Update the shared state with all notes
        self.last_result = note  # Update the last_result attribute
        return f"Note saved: {content}"
