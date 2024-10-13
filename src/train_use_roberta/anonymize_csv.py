import pandas as pd
import re
import csv

# Dictionary for anonymization patterns and their corresponding replacements
anonymization_dict = {
    r"\bChristianity\b|\bAtheism\b|\bJudaism\b|\bIslam\b|\bHinduism\b|\bBuddhism\b": "[Religion]",
    r"\bJesus\b|\bJesus Christ\b|\bProphet Muhammad\b": "[Prophet]",
    r"\bChrist\b|\bAtheist\b|\bJew\b|\bMuslim\b|\bHindu\b|\bBuddhist\b": "[Religion Practitioner]",
    r"\bChristian\b|\bJewish\b|\bMuslima\b": "[Religion Practitioner]",
    r"\bChrists\b|\bAtheists\b|\bJews\b|\bMuslims\b|\bHindus\b|\bBuddhists\b": "[Religion Practitioners]",
    r"\bBible\b|\bQuran\b": "[holy scripture]",
    r"\bGod\b|\bAllah\b|\bVishnu\b|\bShiva\b|\bDevi\b|\bBrahman\b": "[God]",
}


def anonymize_text(text):
    """
    Anonymizes a given text based on predefined patterns.

    :param text: The input text to be anonymized.
    :return: The anonymized text with sensitive information replaced.
    """
    for pattern, replacement in anonymization_dict.items():
        # Replace occurrences of the pattern in the text with the designated replacement
        text = re.sub(
            pattern, replacement, text, flags=re.IGNORECASE
        )  # Perform case-insensitive substitution
    return text


def anonymize_csv_first_column(file_path):
    """
    Anonymizes the first column of a CSV file.

    :param file_path: The path to the input CSV file.
    :return: A pandas DataFrame with the first column anonymized, or None if an error occurs.
    """
    # Attempt to read the CSV file with specific parameters to handle line breaks and quoted cells
    try:
        df = pd.read_csv(
            file_path,
            sep=";",
            quoting=csv.QUOTE_MINIMAL,
            engine="python",
            on_bad_lines="skip",
        )  # Correctly read the CSV
    except pd.errors.ParserError:
        # Print an error message if the CSV cannot be read due to parsing issues
        print("There was a problem reading the CSV file. Check the file format.")
        return None

    # Identify the first column in the DataFrame (assumed to be named 'response')
    first_column = df.columns[0]

    # Apply the anonymization function only to entries in the first column if they are strings
    df[first_column] = df[first_column].apply(
        lambda x: anonymize_text(str(x)) if isinstance(x, str) else x
    )

    return df  # Return the anonymized DataFrame


def main(input_file_path, output_file_path):
    """
    Main function to anonymize the first column of a CSV file and save the result.

    :param input_file_path: The path to the input CSV file.
    :param output_file_path: The path to save the anonymized CSV file.
    """
    # Anonymize the first column of the CSV and save the result to a new file
    anonymized_df = anonymize_csv_first_column(input_file_path)

    if anonymized_df is not None:
        # Save the anonymized DataFrame to a new CSV file
        anonymized_df.to_csv(
            output_file_path, sep=";", index=False, quoting=csv.QUOTE_MINIMAL
        )
        print(f"The anonymized file has been saved to {output_file_path}.")
    else:
        print("Anonymization failed due to issues with the CSV format.")


if __name__ == "__main__":
    input_path = "../../Trained_RoBERTa_Model/Training_and_Test_Data/training_set.csv"  # Update this path as needed
    output_path = "../../Trained_RoBERTa_Model/Training_and_Test_Data/anonymized_training_set.csv"  # Update this path as needed

    main(input_path, output_path)
