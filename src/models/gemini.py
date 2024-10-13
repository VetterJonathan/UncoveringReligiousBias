import os
import google.generativeai as genai
from dotenv import load_dotenv
from src.helpers.json_utils import write_to_json  # Import the JSON function

# Load environment variables from a .env file
load_dotenv()

# Configure the Gemini AI client with your API key
genai.configure(api_key=os.getenv("GOOGLE_GENAI_API_KEY"))

# Safety settings disabled intentionally to prevent blocking during prompt processing
# These settings allow all types of content to be processed without being blocked
safe = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE",
    },
]

# Instantiate a GenerativeModel object with the model name and safety settings
model = genai.GenerativeModel(model_name="gemini-1.5-flash", safety_settings=safe)


def get_gemini_response(prompt):
    """
    Get a response from the Gemini model for a given prompt.

    :param prompt: The prompt to send to the Gemini model.
    :return: The response text from the model, stripped of surrounding whitespace.
    """

    # Start a chat session with an empty history (no prior messages)
    chat_session = model.start_chat(history=[])

    # Send the prompt to the model and get the response
    response = chat_session.send_message(prompt)

    # Return the response text after stripping any surrounding whitespace
    return response.text.strip()


def process_gemini_prompts(input_file, output_file, num_repeats):
    """
    Process prompts from an input file, get responses from the Gemini model, and save the results to a JSON file.

    :param input_file: Path to the input file containing prompts (one per line).
    :param output_file: Path to the output file where results will be saved.
    :param num_repeats: Number of times to repeat each prompt for processing.
    """

    # Read prompts from the input file (assuming one prompt per line)
    with open(input_file, "r") as file:
        prompts = file.readlines()

    results = []  # Initialize an empty list to store the results
    total_prompts = len(prompts)  # Total number of prompts
    total_tasks = (
        total_prompts * num_repeats
    )  # Total number of tasks (prompts * repetitions)

    try:
        # Loop through each prompt from the input file
        for index, prompt in enumerate(prompts):
            # Strip leading/trailing whitespace from the prompt
            prompt = prompt.strip()
            if not prompt:
                continue  # Skip empty lines

            # Repeat the prompt processing for the specified number of times (num_repeats)
            for repeat in range(num_repeats):
                # Get the response from the Gemini model for the current prompt
                response = get_gemini_response(prompt)

                # Store the result in the format: [Prompt Number, Repeat Number, Prompt, Response]
                results.append([index + 1, repeat + 1, prompt, response])

                # Calculate the current task number and print progress
                current_task = (index * num_repeats) + repeat + 1
                print(
                    f"Gemini: Processing Prompt {index + 1}/{total_prompts}, Repetition {repeat + 1}/{num_repeats} ({current_task}/{total_tasks} tasks completed)"
                )

    finally:
        # Ensure results are written to the JSON file even if an error occurs
        write_to_json(output_file, results)
