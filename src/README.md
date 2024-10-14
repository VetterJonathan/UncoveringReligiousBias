# Source Code Directory

This section provides an in-depth overview of the contents and the functionality of each module within this directory, making it easier for anyone using this codebase to understand and navigate the project effectively. This document aims to clarify the purpose and usage of each script, particularly within the context of generating, analyzing, and managing responses from various AI models integrated within the system.

## Directory Structure

The `src` directory is structured into several folders and individual scripts. Each is described below, with detailed instructions on their usage and features.

### Folders and Scripts

#### 1. `analyze_results`

This folder contains scripts to analyze the outputs from language models, focusing on detecting biases and categorizing responses.

- **`detoxify_bias_detection.py`**: 
  - Utilizes the Detoxify package to compute toxicities in responses.
  - Functions include loading JSON data, analyzing responses with biases, filtering based on an acceptance threshold, and writing results to a JSON file.
  - This file is executed within `main_analyze.py` and not standalone.

- **`keywords_detection.py`**:
  - Searches responses for specific keywords associated with bias, particularly violent terms.
  - Must be executed individually due to specific file loading structures.

- **`response_categorization.py`**:
  - Categorizes responses based on predefined rules into the classes: "Answered", "Not Answered", and "Disclaimer".
  - This file is executed within `main_analyze.py` and not standalone.

#### 2. `graphs`

This folder generates graphs and charts that provide visual insights into the analysis results.

- **`answer_categories_radar_chart.py`**:
  - Generates radar charts showing response categorizations across different models.

- **`answer_categories_stacked_barchart.py`**:
  - Produces a stacked bar chart representation with specified confidence intervals.

- **`bias_heatmap.py`**:
  - Creates a heatmap that visually represents bias cases percentages for each religion and model.
  
- **`debate_winners.py`**:
  - Utilizes several data visualization techniques (e.g., barcharts, boxplots) to depict statistics about debate winners per religion across models.
  - Computes standard deviations, total wins, and formats output appropriately, saving images and results in specified file paths.

- **`not_answered_pie_chart.py`**:
  - Constructs pie charts that illustrate the distributions of "Not Answered" categorizations among different models.

#### 3. `helpers`

This folder contains utility scripts that assist in data management and transformations.

- **`csv_utils.py` & `json_utils.py`**:
  - Provide utility functions to write, and ensure unique file naming for both CSV and JSON data operations.

- **`generate_common_name_prompts.py`**:
  - Generates prompts using a template and random selections from name lists to create diverse sets of input queries.
  - Modifiable elements include name file paths, the sentence structure template, and the number of sentences to generate.

#### 4. `models`

This folder involves scripts to interact with specific LLMs for generating responses. (All files are executed within `main_generate_responses.py` and not standalone.)

- **`gemini.py`**: Configures and executes requests to the Gemini model using specified prompts.

- **`gpt.py`**: Interfaces with OpenAI's GPT model for obtaining responses.
- **`mistral.py`**: Handles interactions with the Mistral model, managing inputs and outputs accordingly.

#### 5. `train_use_roberta`

These scripts manage data preparation, training, and utilization of a RoBERTa model for sequence classification.

- **`anonymize_csv.py`**:
  - Anonymizes specific keywords from CSV data based on a provided dictionary of patterns.
  - Essential for preserving data privacy and avoiding unintended biases.

- **`create_training_test_set.py`**:
  - Facilitates the preparation of training and test datasets.
  - Manages file loading, entry selection, and saving to CSV format.
  - Defaults: `training_size_per_classifier` is `1000`, `test_size_per_classifier` is `250`.

- **`json_to_csv_for_roberta_classification.py`**:
  - Converts JSON data into CSV format for easier compatibility with machine learning frameworks.

- **`train_roberta.py`**:
  - Prepares, tokenizes, and trains a RoBERTa classification model.

- **`use_roberta.py`**:
  - Utilizes the trained RoBERTa model for predictions, mapping model output to human-readable labels.
  - Essential pathways and mappings are predefined for effective usage.

#### 6. Main Scripts

The directory includes two main orchestrating scripts that manage distributed operations across multiple modules:

- **`main_analyze.py`**:
  - Centralizes analysis processes across various categorization and bias detection scripts.
  - Allows for streamlined operations without executing each script independently.
  - Default `acceptance_threshold` is `0.20`.

- **`main_generate_responses.py`**: 
  - Coordinates the running of response generation scripts from multiple LLMs simultaneously using multithreading.
  - Specifies input/output parameters and manages process completion efficiently.
  - `repeat_count` defaults to 150 for Generic Prompts and 1 for Name Prompts.

 ## Instructions for Generating Own Data

1. **Setup**: Ensure you have all necessary dependencies installed. Place your `.env` files correctly for storing your API keys relative to each utilized model.

2. **Configuration**: Update file paths and parameters as required within each script, especially in the `__main__` sections. Pay attention to the configuration of prompts and output files in the models folder.

3. **Execution**: 
   - Start with `main_generate_responses.py` to create responses from models.
   - Proceed with `main_analyze.py` for categorization and bias checks.
   - Generate visual insights using scripts in the `graphs` folder.
   - Individually run any additional scripts based on specific analysis or model requirements detailed earlier. 

4. **Adjustments**: The parameters such as repeat_count in prompt generation and acceptance_threshold in analysis can be adjusted to suit specific needs or datasets.

This setup is designed to provide robust capabilities for analyzing and understanding biases in generated content from various LLMs while offering a foundation for extended experiments and modifications.


For further details or clarifications, feel free to explore the comments embedded within the code scripts

Ensure all dependencies are installed and paths are correctly set as per your environment.
