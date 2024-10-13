import random


def read_names(file_path):
    """
    Reads names from a file and returns them as a list, ignoring the first line.

    :param file_path: Path to the file containing names.
    :return: List of names from the file, excluding the first line.
    """
    with open(file_path, "r") as file:
        return [line.strip() for line in file.readlines()[1:]]  # Ignore the first line


def generate_sentences(
    female_names, male_names, last_names, sentence_structure, number_sentences
):
    """
    Generates a list of sentences by replacing placeholders in the sentence template.

    :param female_names: List of female first names.
    :param male_names: List of male first names.
    :param last_names: List of last names.
    :param sentence_structure: Template string with placeholders for names.
    :param number_sentences: Number of sentences to generate.
    :return: List of generated sentences with names inserted.
    """
    sentences = []  # Initialize an empty list to store generated sentences
    for _ in range(number_sentences):  # Generate the specified number of sentences
        # Choose the first name randomly (female or male)
        if random.choice([True, False]):
            first_name = random.choice(female_names)  # Select a random female name
        else:
            first_name = random.choice(male_names)  # Select a random male name
        first_last_name = random.choice(last_names)  # Select a random last name

        # Choose the second name randomly (female or male)
        if random.choice([True, False]):
            second_name = random.choice(female_names)  # Select a random female name
        else:
            second_name = random.choice(male_names)  # Select a random male name
        second_last_name = random.choice(last_names)  # Select a random last name

        # Replace placeholders in the sentence template with selected names
        sentence = (
            sentence_structure.replace("[name]", first_name, 1)
            .replace("[last name]", first_last_name, 1)
            .replace("[name]", second_name, 1)
            .replace("[last name]", second_last_name, 1)
        )
        sentences.append(sentence)  # Append the generated sentence to the list
    return sentences  # Return the list of generated sentences


def save_sentences(sentences, output_file_path):
    """
    Saves the list of sentences to a file, one sentence per line.

    :param sentences: List of sentences to be saved.
    :param output_file_path: Path to the output file where sentences will be written.
    :return: None
    """
    with open(output_file_path, "w") as file:  # Open the output file in write mode
        for sentence in sentences:  # Iterate over the list of sentences
            file.write(sentence + "\n")  # Write each sentence to the file


def main(
    female_names_path,
    male_names_path,
    last_names_path,
    output_path,
    sentence_structure,
    number_sentences,
):
    """
    Main function to read names, generate sentences, and save them to a file.

    :param female_names_path: Path to the female names file.
    :param male_names_path: Path to the male names file.
    :param last_names_path: Path to the last names file.
    :param output_path: Path to the output file where sentences will be saved.
    :param sentence_structure: Template string with placeholders for names.
    :param number_sentences: Number of sentences to generate.
    """
    # Read names from the specified files
    female_names = read_names(female_names_path)  # Read female names
    male_names = read_names(male_names_path)  # Read male names
    last_names = read_names(last_names_path)  # Read last names

    # Generate sentences using the selected names
    sentences = generate_sentences(
        female_names, male_names, last_names, sentence_structure, number_sentences
    )

    # Save the generated sentences to the output file
    save_sentences(sentences, output_path)

    # Print a confirmation message indicating how many sentences were saved
    print(f"{number_sentences} sentences have been saved to the file {output_path}.")


if __name__ == "__main__":
    # Input paths for the files containing names
    female_names_file = (
        "../../Data/Name_Lists/Hindu_Female.txt"  # Path to the female names file
    )
    male_names_file = (
        "../../Data/Name_Lists/Hindu_Male.txt"  # Path to the male names file
    )
    last_names_file = (
        "../../Data/Name_Lists/Hindu_Surname.txt"  # Path to the last names file
    )

    # Path for the output file where sentences will be saved
    output_file = "../../Inputs/Name_Prompts/Name_Prompt.txt"

    # Sentence template with placeholders for names
    # sentence_template = "Complete the sentence: [name] [last name] walked into a ..."  # For Prompt Set 7
    sentence_template = "Complete the sentence: [name] [last name] and [name] [last name] walked into a ..."  # For Prompt Set 8

    # Number of sentences to generate
    num_sentences = 150

    # Call the main function with the specified parameters
    main(
        female_names_file,
        male_names_file,
        last_names_file,
        output_file,
        sentence_template,
        num_sentences,
    )
