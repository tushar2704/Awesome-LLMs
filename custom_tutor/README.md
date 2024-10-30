# AI-Powered Personal Learning Path Generator

This project is an AI-powered tool designed to generate personalized learning paths based on user inputs. It leverages the power of AI to create tailored curriculums and schedules for various educational topics.

## Features

- **Personalized Learning Paths**: Generate custom learning paths based on user preferences and goals.
- **Weekly Schedules**: Detailed weekly schedules with activities and focus areas.
- **Interactive UI**: User-friendly interface built with Streamlit for easy interaction.
- **AI Integration**: Utilizes AI models to create dynamic and personalized content.

## Requirements

- Python 3.7+
- Streamlit
- CrewAI
- Groq
- Dotenv

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/tushar2704/Awesome-LLMs/tree/main/custom_tutor
    cd custom_tutor
    ```

2. Create a virtual environment and install dependencies:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    pip install -r requirements.txt
    ```

3. Set up your environment variables:

    Create a `.env` file in the root directory and add your Groq API key:

    ```
    GROQ_API_KEY=your_api_key_here
    ```

## Usage

1. Run the Streamlit app:

    ```bash
    streamlit run main.py
    ```

2. Open the provided URL in your web browser to access the AI-Powered Personal Learning Path Generator.

## Project Structure

- `main.py`: The main script that runs the Streamlit app.
- `requirements.txt`: List of Python dependencies.
- `.env`: Environment variables file (not included in the repository for security reasons).

## How It Works

1. **User Input**: Users provide their learning topic, specific focus, duration, and hours per week.
2. **AI Generation**: The AI model generates a personalized learning path with weekly schedules and activities.
3. **Display**: The generated learning path is displayed in an interactive and user-friendly format.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contact

For any questions or support, please contact [Tushar Aggarwal](mailto:tushar.27041994@gmail.com).

---

Happy learning! 🚀
