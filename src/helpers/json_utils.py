import json
import os
from datetime import datetime


def get_unique_filename(output_file):
    """
    Generate a unique file name by appending a number or timestamp if the file already exists.

    :param output_file: Original file name.
    :return: A unique file name.
    """
    if not os.path.exists(output_file):
        return output_file  # If file doesn't exist, return the original name

    # Extract the file name and extension
    base, extension = os.path.splitext(output_file)

    # Generate a new file name with a timestamp to avoid overwriting
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    new_file_name = f"{base}_{timestamp}{extension}"

    return new_file_name


def write_to_json(output_file, data):
    """
    Write data to a JSON file, avoiding overwriting by changing the file name if it exists.

    :param output_file: Path to the output JSON file.
    :param data: List of lists, where each inner list represents a row.
    """
    # Get a unique file name if the file already exists
    output_file = get_unique_filename(output_file)

    json_data = []

    # Convert the data into a list of dictionaries
    for row in data:
        json_entry = {
            "Prompt Number": row[0],
            "Repeat Number": row[1],
            "Prompt": row[2],
            "Response": row[3],
        }
        json_data.append(json_entry)

    # Write the JSON data to the output file
    with open(output_file, "w") as jsonfile:
        json.dump(json_data, jsonfile, indent=4)

    print(f"Data written to {output_file}")


def write_bias_to_json(output_file, data):
    """
    Write bias analysis results to a JSON file, avoiding overwriting by changing the file name if it exists.

    :param output_file: Path to the output JSON file.
    :param data: List of dictionaries containing bias results.
    """
    output_file = get_unique_filename(output_file)

    # Create a list to hold the formatted entries
    json_data = []

    for entry in data:
        # Append the formatted entry to the json_data list
        json_data.append(
            {
                "Prompt Number": entry["Prompt Number"],
                "Repeat Number": entry["Repeat Number"],
                "Response": entry["Response"],
                "Result": entry["Result"],
                "Full Results": entry["Full Results"],
                "Manual Review": entry["Manual Review"],
            }
        )

    # Write the JSON data to the output file
    with open(output_file, "w") as jsonfile:
        json.dump(json_data, jsonfile, indent=4)

    print(f"Bias results written to {output_file}")
