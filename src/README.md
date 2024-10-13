# Source Code Directory

This directory contains the source code for the bias detection project. The code is modular, focused on processing data, training models, analyzing responses, and visualizing results.

## Subdirectories

- **analyze_results/**: Scripts for analyzing model responses and detecting bias.
- **helpers/**: Utility functions to assist in data processing and manipulation.
- **models/**: Code to interact with language models like GPT, Gemini, and Mistral.
- **train_use_roberta/**: Scripts to train and use a RoBERTa classification model.
- **graphs/**: Generates visual representations such as charts from the analyzed data.

## Running the Code

1. **Prompt Response Generation**: Use scripts in `models/`.
2. **Result Analysis**: Scripts in `analyze_results/` perform bias detection and response categorization.
3. **Graph Generation**: Use scripts in `graphs/` to visualize analysis results.

### Key Scripts

- **main_generate_responses.py**: Main script to invoke LLMs and save responses.
- **main_analyze.py**: For analyzing categorized data.

Ensure all dependencies are installed and paths are correctly set as per your environment.
