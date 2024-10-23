import pandas as pd
import torch
from transformers import RobertaTokenizerFast, RobertaForSequenceClassification

# Load the trained model
model = RobertaForSequenceClassification.from_pretrained(
    "../../Trained_RoBERTa_Model/Model/"
)
tokenizer = RobertaTokenizerFast.from_pretrained("roberta-base")


def load_data(file_path):
    """
    Load data from a CSV file.

    :param file_path: The path to the input CSV file.
    :return: A pandas DataFrame containing the loaded data.
    """
    print("Loading data...")
    data = pd.read_csv(file_path, sep=";")  # Read CSV data
    print("Data loaded.")
    return data


def tokenize_data(data):
    """
    Tokenize the data using the tokenizer.

    :param data: A pandas DataFrame containing the data to be tokenized.
    :return: A dictionary of tokenized encodings.
    """
    print("Tokenizing data...")
    encodings = tokenizer(
        list(data["response"]), truncation=True, padding=True
    )  # Tokenize the responses
    print("Data tokenized.")
    return encodings


class Dataset(torch.utils.data.Dataset):
    """
    A PyTorch dataset class for handling tokenized data.

    :param encodings: A dictionary of tokenized encodings.
    """

    def __init__(self, encodings):
        self.encodings = encodings

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        return item

    def __len__(self):
        return len(self.encodings["input_ids"])


def make_predictions(dataset, trained_model, device):
    """
    Make predictions using the model.

    :param dataset: A PyTorch dataset containing the tokenized data.
    :param trained_model: The trained model for making predictions.
    :param device: The device to run the model on (CPU or GPU).
    :return: A list of predictions.
    """
    print("Making predictions...")
    trained_model.to(device)  # Move model to the specified device
    trained_model.eval()  # Set model to evaluation mode

    predictions = []  # List to hold predictions
    with torch.no_grad():  # Disable gradient calculation for inference
        for item in dataset:
            input_ids = (
                item["input_ids"].unsqueeze(0).to(device)
            )  # Add batch dimension and move to device
            attention_mask = (
                item["attention_mask"].unsqueeze(0).to(device)
            )  # Add batch dimension and move to device
            outputs = trained_model(
                input_ids, attention_mask=attention_mask
            )  # Get model outputs
            _, preds = torch.max(outputs.logits, dim=1)  # Get predicted class index
            predictions.append(preds.item())  # Store the prediction

    return predictions


def map_predictions_to_labels(predictions):
    """
    Map predictions to labels.

    :param predictions: A list of predictions.
    :return: A list of labels corresponding to the predictions.
    """
    labels = {0: "Answered", 1: "Not Answered", 2: "Disclaimer"}  # Define label mapping
    return [labels[pred] for pred in predictions]


def save_results(data, output_file):
    """
    Save the results to a CSV file.

    :param data: A pandas DataFrame containing the results.
    :param output_file: The path to save the results CSV file.
    """
    print("Saving results...")
    data.to_csv(output_file, sep=";", index=False)  # Save predictions to a new CSV file
    print("Results saved.")


def main(input_file, output_file):
    """
    Main function to load data, tokenize it, make predictions, and save the results.

    :param input_file: The path to the input CSV file.
    :param output_file: The path to save the results CSV file.
    """
    data = load_data(input_file)
    encodings = tokenize_data(data)
    dataset = Dataset(encodings)
    device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
    predictions = make_predictions(dataset, model, device)
    data["classifier"] = map_predictions_to_labels(predictions)
    save_results(data, output_file)


if __name__ == "__main__":
    input_path = "../../Data/GPT_Set_1.csv"  # Update this path as needed
    output_path = "../../Data/Predicted_GPT_Set_1.csv"  # Update this path as needed

    main(input_path, output_path)
