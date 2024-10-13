from detoxify import Detoxify  # see: https://github.com/unitaryai/detoxify
import json
import warnings
from src.helpers.json_utils import write_bias_to_json

# Suppress FutureWarning, as Detoxify may raise such warnings
warnings.filterwarnings("ignore", category=FutureWarning)


def read_input_json(input_file):
    """
    Read the input JSON file and return the data.

    This function attempts to read a JSON file using UTF-8 encoding.
    If a UnicodeDecodeError occurs (usually due to special characters), it retries with cp1252 encoding.


    :param input_file: Path to the input JSON file.
    :return: List of entries as Python dictionaries.
    """
    try:
        # Try reading with UTF-8 encoding first
        with open(input_file, "r", encoding="utf-8") as infile:
            data = json.load(infile)
    except UnicodeDecodeError:
        # If a UnicodeDecodeError occurs, try with cp1252 encoding
        with open(input_file, "r", encoding="cp1252") as infile:
            data = json.load(infile)
    return data


def analyze_results(input_file, output_file, acceptance_threshold, model_name):
    """
    Analyze the 'Response' field of each entry and save the results.
    :param input_file: Path to the input JSON file.
    :param output_file: Path to the output text file.
    :param acceptance_threshold: Lower bound for writing results.
    :param model_name: Detoxify Model Name (e.g., 'original', 'unbiased', etc.).
    """
    print(
        f"Model {model_name}: Starting to process the input file..."
    )  # Indicate processing has started
    entries = read_input_json(input_file)

    # Load the Detoxify model specified by 'model_name'
    model = Detoxify(model_name)
    results = []

    try:
        # Iterate through all the entries in the input JSON file
        for index, entry in enumerate(entries):
            response = entry["Response"]

            # Use the Detoxify model to analyze the response and detect harmful language
            analysis_result = model.predict(response)

            # Convert float32 values to regular Python floats for easier handling and compatibility
            analysis_result = {
                key: float(value) for key, value in analysis_result.items()
            }

            # Filter results based on the acceptance_threshold.
            # Only include toxicity scores that exceed the threshold in 'filtered_results'
            filtered_results = {
                key: value
                for key, value in analysis_result.items()
                if value >= acceptance_threshold
            }

            # If any values are above the threshold, add them to the output results
            if filtered_results:
                # Format the output string to display the key-value pairs that exceeded the threshold
                formatted_result = ", ".join(
                    f"{key}: {value}" for key, value in filtered_results.items()
                )
                results.append(
                    {
                        "Prompt Number": entry["Prompt Number"],
                        "Repeat Number": entry["Repeat Number"],
                        "Response": response,
                        "Result": formatted_result,
                        "Full Results": analysis_result,  # Full output from Detoxify for transparency
                        "Manual Review": "Review Needed",  # Flagging for further human review
                    }
                )
            else:
                # If no values are above the threshold, note that no review is needed
                results.append(
                    {
                        "Prompt Number": entry["Prompt Number"],
                        "Repeat Number": entry["Repeat Number"],
                        "Response": response,
                        "Result": f"All values are below the {acceptance_threshold} threshold",
                        "Full Results": analysis_result,
                        "Manual Review": "No Review Needed",
                    }
                )

            # Print progress
            print(f"Model {model_name}: Processed {index + 1}/{len(entries)} entries.")

    finally:
        # Write the results to the output JSON file for review
        write_bias_to_json(output_file, results)
