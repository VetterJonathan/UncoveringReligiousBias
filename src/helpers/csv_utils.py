import csv
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


def write_to_csv(output_file, data):
    """
    Write data to a CSV file, avoiding overwriting by changing the file name if it exists.

    :param output_file: Path to the output CSV file.
    :param data: List of lists, where each inner list represents a row.
    """
    # Get a unique file name if the file already exists
    output_file = get_unique_filename(output_file)

    with open(output_file, "w", newline="") as csvfile:
        # Initialize CSV writer with a semicolon as the delimiter
        csv_writer = csv.writer(csvfile, delimiter=";")
        # Write the header row
        csv_writer.writerow(["Prompt Number", "Repeat Number", "Prompt", "Response"])
        # Write all rows of data
        csv_writer.writerows(data)

        print(f"Data written to {output_file}")


def write_bias_to_csv(output_file, data):
    """
    Write bias analysis results to a CSV file, avoiding overwriting by changing the file name if it exists.

    :param output_file: Path to the output CSV file.
    :param data: List of dictionaries containing bias results.
    """
    # Get a unique file name if the file already exists
    output_file = get_unique_filename(output_file)

    with open(output_file, "w", newline="") as csvfile:
        # Initialize CSV writer with a semicolon as the delimiter
        csv_writer = csv.writer(csvfile, delimiter=";")
        # Write the header row
        csv_writer.writerow(
            [
                "Prompt Number",
                "Repeat Number",
                "Response",
                "Result",
                "Full Results",
                "Manual Review",
            ]
        )
        # Write all rows of data
        for entry in data:
            csv_writer.writerow(
                [
                    entry["Prompt Number"],
                    entry["Repeat Number"],
                    entry["Response"],
                    entry["Result"],
                    entry["Full LLM_Output"],
                    entry["Manual Review"],
                ]
            )

        print(f"Bias results written to {output_file}")
