# Results Directory Documentation

This directory contains the output data of various experiments and analyses performed using different LLMs. The folder is structured into subdirectories based on the type of analysis and the model used. Below is a detailed guide to understanding and navigating the contents.
  


## Folder Structure

The `Results` folder is organized into the following subdirectories:

1. **Answer_Categorization**: Contains categorized responses from models.
   - **Gemini**: Output from the Gemini 1.5 Flash model.
   - **GPT**: Output from the GPT-4o mini model.
   - **Mistral**: Output from the Mistral NeMo model.
   - Sub-subdirectories are organized by Prompt Sets (e.g., `Prompt_Set_1`, `Prompt_Set_2`, etc.).
     - Files: `answered.json`, `disclaimer.json`, `not_answered.json`, and `uncategorized.json`.

2. **Bias_Detection**: Contains bias detection results.
   - Each model (Gemini, GPT, Mistral) has outputs using 'original' and 'unbiased' configurations of the detoxify model.
   - Subdirectories contain `.json` files with results specific to each prompt set like `Prompt_Set_1_Bias_Score.json`.

3. **Keywords_List**: Houses results from keyword detection analysis.
   - Files like `Keywords_Results_Gemini.json` for Gemini model outputs include detected violent keywords.

4. **LLM_Output**: Raw outputs from the LLM responses, organized by model and prompt set.
   - Examples include `Gemini_Prompt_Set_1_Results.json` for the Gemini model's raw responses.

## JSON File Structure

Each `.json` file contains entries related to different analysis aspects. Below are the fields you may encounter:

### Common Fields:
- **Prompt Number**: Identifies the line number of the prompt in the input file.
- **Repeat Number**: Indicates how many times the prompt was reiterated.
- **Prompt**: The exact text used to query the model.
- **Response**: The model's generated output for the specified prompt.

### Additional Fields in Category Specific JSONs:

#### Answer Categorization:
- **ClassificationRule**: Rule applied for categorizing the response.

#### Bias Detection:
- **Result**: A summary stating whether any bias scores exceed a set threshold, and if so, the specific categories exceeding it.
- **Full Results**: Detailed scores for each category evaluated by the detoxify model.
- **Manual Review**: Specifies if a manual review is required (`Review Needed`), not required (`No Review Needed`), or if the review has already been conducted (`True` if bias is present, `False` if not).


#### Keyword List:
- **Name**: Denotes the source file name for the result entry.
- **Violent Words**: Lists keywords from a detection list found in the response.
- **Manual Review**: Specifies if that manual review is required (`Review Needed`), or if the review has already been conducted (`True` if violent words are present, `False` if not).
