from config import AgentConfig
from agent import Agent
from groq import Groq
import os
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def decompose_tasks(paragraph: str) -> list:
    """
    Sends the task paragraph to the Groq API for decomposition.
    :param paragraph: A string containing the task paragraph.
    :return: A list of decomposed tasks.
    """
    # Initialize Groq client
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    # Define the LLM prompt for decomposition
    decomposition_prompt = f"""
    Decompose the following task, which is a paragraph, into a list of clear, concise tasks so that they can be fed to a list for further processing. 
    Group all tasks under one '##' and terminate the task list with '__'. 
    Ensure no extra text is generated outside of this structure.
    Paragraph: "{paragraph}"
    Tasks:
    ## 
    Task 1: Perform the first task here.
    Task 2: Perform the second task here.
    __
    """

    try:
        logger.info("Sending decomposition prompt to Groq API.")
        # Send the decomposition request to the Groq API
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": decomposition_prompt,
                }
            ],
            model="llama3-8b-8192",
        )

        # Extract the response content
        response_text = chat_completion.choices[0].message.content
        logger.info(f"Received response from Groq API: {response_text}")

        # Parse the response to extract tasks
        tasks = []
        if response_text.startswith("##") and response_text.endswith("__"):
            task_lines = response_text.strip("##").strip("__").strip().split("\n")
            tasks = [line.strip() for line in task_lines if line.strip().startswith("Task")]
        logger.info(f"Decomposed tasks: {tasks}")
        return tasks

    except Exception as e:
        logger.error(f"Error during task decomposition: {str(e)}")
        return []

def main():
    # Initialize the agent configuration
    config = AgentConfig(
        role="Video Editing Task Agent",
        api_token=os.getenv("GROQ_API_KEY"),  # Use the Groq API key
        model_id="llama3-8b-8192"  # Ensure the model ID matches your Groq setup
    )

    # Input paragraph containing tasks
    task_paragraph = """get video meta data for the given video"""

    logger.info("Starting task decomposition.")
    # Decompose the paragraph into tasks using the Groq API
    tasks = decompose_tasks(task_paragraph)

    if not tasks:
        logger.error("No tasks were decomposed. Exiting.")
        return

    # Initialize the main agent
    agent = Agent(config)

    logger.info("Processing tasks with the agent.")
    # Process each decomposed task using the agent
    for task in tasks:
        logger.info(f"Processing task: {task}")
        result = agent.run(task)
        logger.info(f"Result for task '{task}': {result}")
        print(f"\nTask: {task}")
        print(f"Result: {result}")

if __name__ == "__main__":
    main()
