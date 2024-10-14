# Weather Chatbot

This Weather Chatbot is a Python-based application that provides weather information for any location in the world, for past dates, current day, and up to 6 days in the future. It also engages in general conversation using OpenAI's GPT model.

## Features

- Retrieve weather information for any location worldwide
- Provide historical weather data for past dates
- Offer current weather conditions
- Forecast weather for up to 6 days in the future
- Engage in general conversation using AI

## Prerequisites

Before running the chatbot, make sure you have the following:

- Python 3.6 or higher
- Required Python packages (install using `pip install -r requirements.txt`):
  - requests
  - openai
  - python-dotenv
  - dateparser

## API Keys and Environment Variables

The chatbot uses several APIs. You'll need to obtain API keys for the following services:

- OpenAI API
- Meteoblue API
- OpenCage Geocoding API
- Visual Crossing Weather API

Create a `.env` file in the project root directory with the following content, replacing the placeholder values with your actual API keys:

```
OPENAI_API_KEY=your_openai_api_key_here
METEOBLUE_API_KEY=your_meteoblue_api_key_here
OPENCAGE_API_KEY=your_opencage_api_key_here
VISUALCROSSING_API_KEY=your_visualcrossing_api_key_here
```

## Installation

1. Clone this repository or download the source code.
2. Navigate to the project directory.
3. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```
4. Install the required packages:
   ```
   pip install -r requirements.txt
   ```
5. Create the `.env` file with your API keys as described in the previous section.

## Usage

To run the chatbot, execute the following command in your terminal:

```
python weather_chatbot.py
```

Once the chatbot is running:

1. You'll see a welcome message.
2. Type your questions or statements.
3. The chatbot will respond with weather information or engage in general conversation.
4. To exit the chatbot, type 'exit'.

## Examples

Here are some example queries you can try:

- "What's the weather like in New York today?"
- "Tell me the weather forecast for London next Monday."
- "What was the weather like in Paris on July 14, 2022?"
- "How's the weather in Tokyo tomorrow?"

## Project Structure

- `weather_chatbot.py`: Main script containing the chatbot logic
- `.env`: File containing environment variables (API keys)
- `requirements.txt`: List of required Python packages

## Limitations

- The chatbot can only provide weather forecasts for up to 6 days in the future.
- Historical weather data availability may vary depending on the location and date requested.

## Troubleshooting

If you encounter any issues:

1. Ensure all API keys in the `.env` file are correctly set and valid.
2. Check your internet connection.
3. Verify that all required packages are installed correctly.
4. Make sure the `.env` file is in the same directory as the `weather_chatbot.py` script.

## License

This project is licensed under the MIT License.

## Acknowledgments

- Warm thanks to Sasha and Fabian for providing the tasks
- OpenAI for providing the GPT model
- Meteoblue for weather forecast data
- OpenCage for geocoding services
- Visual Crossing for historical weather data

For any questions or support, please open an issue in the GitHub repository.