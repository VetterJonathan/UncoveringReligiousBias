  # Results Directory

   Stores results from all LLM interactions and subsequent analyses, including response categorizations, bias detection, and keyword detection.

   ## Subdirectories Structure

   - `Answer_Categorization/`: JSON files detailing categorized responses from various models.
   - `Bias_Detection/`: JSON files capturing the bias analysis results for each model's output.
   - `Keywords_List/`: JSON files indicating whether specific violent keywords were detected within the responses.
   - `LLM_Output/`: JSON files housing raw outputs from the AI models used in the project.

   ## File Format

   - Each JSON file contains entries with prompt numbers, prompts, responses, and classification details.
   - The naming conventions highlight the prompt sets and models tested.

   ## Utilization

   These results feed into other project components for data visualization and further analysis.
