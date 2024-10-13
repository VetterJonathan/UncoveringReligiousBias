import os
import json
import random
import csv


def load_json_files(directory):
    """
    Load all entries from the .json files in the directory structure

    :param directory: The directory containing the JSON files.
    :return: A dictionary with classifiers as keys and lists of entries as values.
    """
    classifiers = [
        "answered.json",
        "disclaimer.json",
        "not_answered.json",
    ]  # List of classifier files
    # Initialize a dictionary to hold lists for each classifier
    data = {classifier.replace(".json", ""): [] for classifier in classifiers}

    # Traverse the directory structure
    for root, dirs, files in os.walk(directory):
        for classifier in classifiers:
            # Check if the classifier file exists in the current directory
            if classifier in files:
                file_path = os.path.join(root, classifier)  # Construct full file path
                with open(file_path, "r", encoding="utf-8") as f:
                    try:
                        entries = json.load(f)  # Load JSON data
                        data[classifier.replace(".json", "")].extend(
                            entries
                        )  # Add entries to the corresponding classifier list
                    except json.JSONDecodeError as e:
                        print(
                            f"Error decoding {file_path}: {e}"
                        )  # Handle JSON decoding errors
    return data


def select_entries(data, count_per_classifier):
    """
    Select a random set of entries per classifier, ensuring no duplicates

    :param data: Dictionary containing entries for each classifier.
    :param count_per_classifier: Number of entries to select for each classifier.
    :return: A list of selected entries formatted for CSV output.
    """
    selected_entries = []  # Initialize list to hold selected entries
    for classifier, entries in data.items():
        # Check if there are enough entries for the requested count
        if len(entries) < count_per_classifier:
            print(
                f"Warning: Not enough entries for classifier '{classifier}'. Requested {count_per_classifier}, but found {len(entries)}."
            )
        random.shuffle(entries)  # Shuffle the entries to ensure randomness
        # Format selected entries into a list of dictionaries
        selected_entries.extend(
            [
                {
                    "response": f"{entry['Prompt']} -> {entry['Response']}",
                    "classifier": classifier,
                }
                for entry in entries[:count_per_classifier]
            ]  # Select the requested number of entries
        )
    return selected_entries


def save_to_csv(filename, data):
    """
    Save the selected entries to a CSV file with the specified format

    :param filename: The name of the output CSV file.
    :param data: The list of data entries to be saved.
    """
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["response", "classifier"], delimiter=";")
        writer.writeheader()
        writer.writerows(data)


def create_training_and_test_set(
    input_dir,
    training_set_output_path,
    test_set_output_path,
    training_entries_per_classifier,
    test_entries_per_classifier,
):
    """
    Main function to orchestrate the loading, selecting, and saving of entries.

    :param input_dir: The directory containing the input JSON files.
    :param training_set_output_path: The file path for the training set output CSV.
    :param test_set_output_path: The file path for the test set output CSV.
    :param training_entries_per_classifier: The number of training entries to select per classifier.
    :param test_entries_per_classifier: The number of test entries to select per classifier.
    """

    # Load all the data from the specified directory
    data = load_json_files(input_dir)

    # Select entries for the training set
    entries_training = select_entries(data, training_entries_per_classifier)

    # Update the data by removing the selected entries to prevent reuse
    for entry in entries_training:
        classifier = entry["classifier"]  # Get the classifier for the current entry
        # Filter out the selected entries from the original data
        data[classifier] = [
            d
            for d in data[classifier]
            if not (d["Prompt"] + d["Response"]) in entry["response"]
        ]

    # Select entries for the test set
    entries_test = select_entries(data, test_entries_per_classifier)

    # Save the entries to the specified CSV files
    save_to_csv(training_set_output_path, entries_training)
    save_to_csv(test_set_output_path, entries_test)


if __name__ == "__main__":
    # Get the paths for input and output files
    input_directory = (
        "../../Results/Answer_Categorization"  # Input directory for JSON files
    )
    output_file_training = "../../Trained_RoBERTa_Model/Training_and_Test_Data/training_set.csv"  # Output file for training set
    output_file_test = "../../Trained_RoBERTa_Model/Training_and_Test_Data/test_set.csv"  # Output file for test set

    # Set the sizes for training and test sets
    training_size_per_classifier = 1000  # Number of training entries per classifier
    test_size_per_classifier = 250  # Number of test entries per classifier

    # Run the main function with the provided paths and sizes
    create_training_and_test_set(
        input_directory,
        output_file_training,
        output_file_test,
        training_size_per_classifier,
        test_size_per_classifier,
    )
