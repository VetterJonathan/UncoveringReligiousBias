# Towards Fair Representation:<br>Uncovering Biases in AI's Representation of Religion

This repository contains the code, data, and results related to the master's thesis on uncovering biases in AI's representation of religion. The project aims to analyze the outputs of different Large Language Models to detect biases and categorize responses based on prompts related to various religions.

## Repository Structure

- `Data/`: Contains graph images, name lists, and tables summarizing various results.  
  *(This folder includes its own README with details about the files and structure.)*
  
- `Inputs/`: Includes the prompt sets used to generate responses.  
  *(This folder includes its own README with explanations about the prompts and setup.)*

- `Results/`: Contains generated outputs from models, categorized responses, bias detection results, and keyword analysis.  
  *(This folder includes its own README explaining how the results are organized.)*

- `src/`: Source code, organized into modules for model handling, data analysis, and graph generation.  
  *(This folder includes its own README with detailed documentation of each module.)*

- `Trained_RoBERTa_Model/`: Contains all components required for training, anonymizing, testing, and employing a RoBERTa model for the response classification task.   
  *(This folder includes its own README with details on model training and dataset usage.)*

- `requirements.txt`: A list of Python dependencies required for the project.

- `.env.example`: A template for the environment variables necessary for API access.

- `.gitattributes`: Specifies the files tracked by Git Large File Storage (LFS), including the large model file `model.safetensors`. This file ensures that large files are handled properly by Git LFS and not stored directly in the Git repository.

- `Towards_Fair_Representaion_Uncovering_Biases_in_AIs_Represenation_of_Religion.pdf`: The full thesis document.

## Getting Started

To run this project, ensure you have Python 3.x installed along with the required packages listed in `requirements.txt`. Set up your `.env` file using the `.env.example` template and provide the necessary API keys.

### Setting Up the Environment

1. Create an .env file
    ```bash
    cp .env.example .env
    ```
   
2. Add your keys to the .env file

3. Install requirements
    ```bash
    pip install -r requirements.txt
    ```

For detailed information of each module, refer to their respective documentation in the subdirectories.

## Acknowledgements

This research was supported by the Area Information Systems, Prof. Dr. Kevin Bauer, University of Mannheim.