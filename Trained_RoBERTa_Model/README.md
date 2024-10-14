# Trained RoBERTa Model Directory

This directory contains all necessary components for training, anonymizing, testing, and employing a RoBERTa model for the response classification task of this thesis.

## Structure

- `Training_and_Test_Data/`: Raw and processed training and test data, formatted as CSV files.
  - `anonymized_training_set.csv`: An anonymized training set containing 3,000 samples with 1,000 samples for each category. The two columns are `response` and `classifier`.
  - `test_set.csv`: A test set containing 250 samples for each category. The two columns are `response` and `classifier`.
  - `training_set.csv`: An unanonymized training set containing 3,000 samples with 1,000 samples for each category. The two columns are `response` and `classifier`.
- `logs/`: The logs of the training process will be saved here.
- `Trained_RoBERTa_Model/`: This folder will store the trained RoBERTa model once it is trained.

## Usage

### Training the RoBERTa Model

Train the RoBERTa model with:

```bash
python src/train_use_roberta/train_roberta.py
```

### Utilize the Trained RoBERTa Model

To make predictions with the trained RoBERTa model, adjust the path in `src/train_use_roberta/use_roberta.py` to point to the `.csv` file that you want to classify, then execute the following command:


```bash
python src/train_use_roberta/use_roberta.py
```
