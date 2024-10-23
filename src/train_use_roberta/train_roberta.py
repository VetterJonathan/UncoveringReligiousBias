import pandas as pd
from transformers import (
    RobertaTokenizerFast,
    RobertaForSequenceClassification,
    Trainer,
    TrainingArguments,
)
import torch
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
import numpy as np


# Load training and test data from CSV files
def load_data(training_set_path, test_set_path):
    """
    Load training and test data from CSV files.

    :param training_set_path: The path to the training CSV file.
    :param test_set_path: The path to the test CSV file.
    :return: A tuple containing the training and test data as pandas DataFrames.
    """
    print("Loading data...")
    train_data = pd.read_csv(training_set_path, sep=";")  # Load training data
    test_data = pd.read_csv(test_set_path, sep=";")  # Load test data
    print("Data loaded.")
    return train_data, test_data


# Map string labels to integer values for classification
def map_labels(train_data, test_data):
    """
    Map string labels to integer values for classification.

    :param train_data: The training data as a pandas DataFrame.
    :param test_data: The test data as a pandas DataFrame.
    :return: A tuple containing the training and test data with mapped labels.
    """
    labels = {
        "answered": 0,
        "not_answered": 1,
        "disclaimer": 2,
    }  # Define a mapping of labels to integers
    train_data["classifier"] = train_data["classifier"].map(
        labels
    )  # Apply mapping to the training set
    test_data["classifier"] = test_data["classifier"].map(
        labels
    )  # Apply mapping to the test set
    return train_data, test_data


# Tokenize the text data using RoBERTa tokenizer
def tokenize_data(train_data, test_data):
    """
    Tokenize the text data using RoBERTa tokenizer.

    :param train_data: The training data as a pandas DataFrame.
    :param test_data: The test data as a pandas DataFrame.
    :return: A tuple containing the tokenized training and test encodings.
    """
    print("Tokenizing data...")
    tokenizer = RobertaTokenizerFast.from_pretrained(
        "roberta-base", clean_up_tokenization_spaces=True
    )  # Load the RoBERTa tokenizer
    train_encodings = tokenizer(
        list(train_data["response"]), truncation=True, padding=True
    )  # Tokenize training responses
    test_encodings = tokenizer(
        list(test_data["response"]), truncation=True, padding=True
    )  # Tokenize test responses
    print("Data tokenized.")
    return train_encodings, test_encodings


# Create a custom PyTorch dataset class for the training and testing data
class Dataset(torch.utils.data.Dataset):
    """
    Custom PyTorch dataset class for the training and testing data.

    :param encodings: The tokenized encodings.
    :param labels: The labels for the data.
    """

    def __init__(self, encodings, labels):
        self.encodings = encodings  # Store the encoded inputs
        self.labels = labels  # Store the labels

    def __getitem__(self, idx):
        # Create a dictionary of input features for the model
        item = {
            key: torch.tensor(val[idx]) for key, val in self.encodings.items()
        }  # Convert encoding to tensors
        item["labels"] = torch.tensor(
            self.labels.iloc[idx]
        )  # Add the corresponding label as a tensor
        return item  # Return the constructed item

    def __len__(self):
        return len(self.labels)  # Return the total number of samples in the dataset


# Initialize datasets for training and testing
def create_datasets(train_encodings, test_encodings, train_data, test_data):
    """
    Initialize datasets for training and testing.

    :param train_encodings: The tokenized training encodings.
    :param test_encodings: The tokenized test encodings.
    :param train_data: The training data as a pandas DataFrame.
    :param test_data: The test data as a pandas DataFrame.
    :return: A tuple containing the training and test datasets.
    """
    train_dataset = Dataset(
        train_encodings, train_data["classifier"]
    )  # Create dataset for training
    test_dataset = Dataset(
        test_encodings, test_data["classifier"]
    )  # Create dataset for testing
    return train_dataset, test_dataset


# Load the pre-trained RoBERTa model for sequence classification
def load_model():
    """
    Load the pre-trained RoBERTa model for sequence classification.

    :return: The loaded RoBERTa model.
    """
    model = RobertaForSequenceClassification.from_pretrained(
        "roberta-base", num_labels=3
    )  # Load model with 3 output labels
    return model


# Define training arguments for the Trainer
def define_training_args(output_directory, logging_directory):
    """
    Define training arguments for the Trainer.

    :param output_directory: The directory to save the model.
    :param logging_directory: The directory to save the logs.
    :return: The training arguments.
    """
    training_args = TrainingArguments(
        output_dir=output_directory,  # Directory to save the model
        num_train_epochs=3,  # Number of epochs for training
        per_device_train_batch_size=8,  # Batch size for training
        per_device_eval_batch_size=16,  # Batch size for evaluation
        logging_dir=logging_directory,  # Directory to save logs
        logging_steps=10,  # Log every 10 steps
        eval_strategy="epoch",  # Evaluate at the end of each epoch
    )
    return training_args


def compute_metrics(eval_pred):
    """
    Compute Accuracy, Precision, Recall and F1-Score for model predictions.

    :param eval_pred: Tuple of (logits, labels)
    :return: A dictionary of computed metrics.
    """
    logits, labels = eval_pred
    predictions = np.argmax(logits, axis=-1)

    accuracy = accuracy_score(labels, predictions)
    precision, recall, f1, _ = precision_recall_fscore_support(
        labels, predictions, average="weighted"
    )

    return {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1": f1,
    }


def initialize_trainer(model, training_args, train_dataset, test_dataset):
    """
    Initialize the Trainer with the model and dataset for evaluation, including metrics.

    :param model: The loaded RoBERTa model.
    :param training_args: The training arguments.
    :param train_dataset: The training dataset.
    :param test_dataset: The test dataset.
    :return: The initialized Trainer.
    """
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=test_dataset,
        compute_metrics=compute_metrics,
    )
    return trainer


# Start the training process
def train_model(trainer):
    """
    Start the training process.

    :param trainer: The initialized Trainer.
    """
    print("Starting training...")
    trainer.train()  # Execute the training
    print("Training completed.")


# Evaluate the model on the test set
def evaluate_model(trainer):
    """
    Evaluate the model using the test dataset and print the results.

    :param trainer: The initialized Trainer.
    """
    print("Evaluating model on test data...")
    eval_results = trainer.evaluate()
    print(eval_results)


def save_model(model, output_directory):
    """
    Save the trained model to the specified directory.

    :param model: The trained model.
    :param output_directory: The directory to save the model.
    """
    print("Saving model...")
    model.save_pretrained(output_directory)
    print("Model saved.")


def main(training_set_path, test_set_path, output_directory, logging_directory):
    """
    Main function to load data, tokenize, train the model, and save the model.

    :param training_set_path: The path to the training CSV file.
    :param test_set_path: The path to the test CSV file.
    :param output_directory: The directory to save the model.
    :param logging_directory: The directory to save the logs.
    """
    train_data, test_data = load_data(training_set_path, test_set_path)
    train_data, test_data = map_labels(train_data, test_data)

    if (
        train_data["classifier"].isnull().values.any()
        or test_data["classifier"].isnull().values.any()
    ):
        print(
            "There are NaN values in the labels. Please handle them before proceeding."
        )
    else:
        train_encodings, test_encodings = tokenize_data(train_data, test_data)
        train_dataset, test_dataset = create_datasets(
            train_encodings, test_encodings, train_data, test_data
        )
        model = load_model()
        training_args = define_training_args(output_directory, logging_directory)
        trainer = initialize_trainer(model, training_args, train_dataset, test_dataset)

        # Train the model
        train_model(trainer)

        # Save the model after training
        save_model(model, output_directory)

        # Evaluate the model on the test dataset
        evaluate_model(trainer)


if __name__ == "__main__":
    train_path = "../../Trained_RoBERTa_Model/Training_and_Test_Data/anonymized_training_set.csv"  # Update this path as needed
    test_path = "../../Trained_RoBERTa_Model/Training_and_Test_Data/test_set.csv"  # Update this path as needed
    output_dir = "../../Trained_RoBERTa_Model/Model/"  # Update this path as needed
    logging_dir = "../../Trained_RoBERTa_Model/Model/logs"  # Update this path as needed

    main(train_path, test_path, output_dir, logging_dir)
