from config import AgentConfig
from agent import Agent
from api_client import HuggingFaceAPI

def decompose_tasks(paragraph: str, llm_client: HuggingFaceAPI) -> list:
    """
    Sends the task paragraph to the LLM for decomposition.
    :param paragraph: A string containing the task paragraph.
    :param llm_client: An instance of HuggingFaceAPI to handle the LLM call.
    :return: A list of decomposed tasks.
    """
    # Define the LLM prompt for decomposition
    decomposition_prompt = f"""
    Decompose the following task, which is a paragraph, into a list of clear, concise tasks so that they can be fed to a list for further processing. 
    Mark the start the task listing with '##' and the end of the task listings with '__'. 
    Ensure no extra text is generated outside of this structure.
    Paragraph: "{paragraph}"
    Tasks:
    ## 
     Task 1: Perform the first task here.
     Task 2: Perform the second task here.
    __
    """

    try:
        # Send the decomposition request to the LLM
        response = llm_client.generate_response(decomposition_prompt)

        # Parse the LLM response into a list of tasks
        tasks = [
            task.strip("##").strip(" __").strip()
            for task in response.split("##") if task.strip() and task.endswith("__")
        ]
        return tasks
    except Exception as e:
        print(f"Error during task decomposition: {str(e)}")
        return []

def main():
    # Initialize the agent configuration
    config = AgentConfig(
        role="Python Task Agent",
        api_token="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"  # Replace with your Hugging Face API token
    )
    # Initialize the Hugging Face client for LLM calls
    llm_client = HuggingFaceAPI(config)

    # Input paragraph containing tasks
    task_paragraph = """
    Calculate 2 + 2 and save the result as a note. 
    Then, calculate 10 * 5 and save it. 
    Finally, write a small poem and save it.
    """

    # Decompose the paragraph into tasks using the LLM
    tasks = decompose_tasks(task_paragraph, llm_client)
    # Initialize the main agent
    agent = Agent(config)

    # Process each decomposed task using the agent
    for task in tasks:
        print(f"\nTask: {task}")
        result = agent.run(task)
        print(f"Result: {result}")

if __name__ == "__main__":
    main()
