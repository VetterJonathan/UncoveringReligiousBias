import json
import pandas as pd


def json_to_csv(json_file, csv_file):
    """
    Converts JSON data to a CSV file.

    :param json_file: The path to the input JSON file to be converted.
    :param csv_file: The path where the output CSV file will be saved.
    """
    # Read the JSON file
    with open(json_file, "r") as file:
        data = json.load(file)

    # Check if the loaded data is a list
    if isinstance(data, list):
        # Extract Prompt and Response from each object in the list and combine them
        responses = [f"{entry['Prompt']} -> {entry['Response']}" for entry in data]
    else:
        # If the data is not a list, assume it is a single dictionary
        responses = [f"{data['Prompt']} -> {data['Response']}"]

    # Create a DataFrame for the CSV with responses and an empty field for classifiers
    df = pd.DataFrame(
        {
            "response": responses,
            "classifier": [""]
            * len(responses),  # Initialize an empty field for classifier
        }
    )

    # Save the DataFrame to a CSV file with semicolon as the delimiter
    df.to_csv(csv_file, index=False, sep=";")
    print(f'The CSV file has been successfully created at "{csv_output_file}".')


if __name__ == "__main__":
    json_input_file = "../../Results/LLM_Output/GPT/GPT_Prompt_Set_1_Results.json"  # Update this path as needed
    csv_output_file = "../../Data/GPT_Set_1.csv"  # Update this path as needed

    json_to_csv(json_input_file, csv_output_file)
