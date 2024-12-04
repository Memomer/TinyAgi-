# tinyAgi

## Overview

Welcome to the **TinyAgi-** repository! This project is built to help you learn and explore the capabilities of agentic frameworks. It provides a hands-on approach to understanding how these systems operate, enabling you to build tools and experiment with novel research methodologies in artificial intelligence.

## Learning Objectives

- **Explore Agentic Frameworks**: Delve into the architecture and functionality of agentic systems, gaining a comprehensive understanding of their capabilities.
- **Build and Integrate Tools**: Learn how to create and integrate various tools that enhance the functionality of AI agents.
- **Experiment with Research**: Engage with cutting-edge research in AI, applying it to practical tasks to deepen your knowledge and skills.

## Project Structure

The project consists of several key components:

- **main.py**: The main entry point for the application, where tasks are decomposed and processed using a Hugging Face API client. Update this file with your own tasks to run the application on your specific needs.
- **agent.py**: Contains the `Agent` class, which defines the behavior of the AI agent, including how it processes tasks and generates executable Python code.
- **editor/**: A folder containing tools like the video editing tool, which can be customized and extended for various multimedia tasks.

## Getting Started

To get started with tinyAgi, follow these steps:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Memomer/TinyAgi-.git
   cd tinyAgi
   ```

2. **Set Up Environment**:
   Ensure you have Python installed and set up a virtual environment. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure API Access**:
   Create a `.env` file in the root directory and add your Hugging Face API key:
   ```
   HUGGINGFACE_API_KEY=your_api_key_here
   ```

4. **Run the Application**:
   Execute the main script to start decomposing tasks:
   ```bash
   python agents_hf/main.py
   ```

## To be added 

- **Custom Tool Creation**: Easily create and integrate custom tools tailored to your specific needs. The project includes an inbuilt video editing tool located in the `editor` folder.
- **Multi-Modal Support**: The framework supports various input and output modalities, allowing for a more versatile interaction with tasks.
- **Transcription Capabilities**: Built-in support for transcribing audio and video content into text, facilitating easier task decomposition and processing.
- **Task Customization**: Update `main.py` with your own tasks to run the application on custom inputs, allowing for personalized experimentation.
- **More Features to be Added**: The project is continuously evolving, with plans to introduce additional features and tools in the future.


## Contributing

We welcome contributions! If you have ideas for improvements or new features, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

## Acknowledgments

Thanks to the open-source community and the researchers whose work inspires this project. Let's learn and innovate together!
