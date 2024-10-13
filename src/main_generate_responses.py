from src.models.gpt import process_gpt_prompts
from src.models.gemini import process_gemini_prompts
from src.models.mistral import process_mistral_prompts
import concurrent.futures

if __name__ == "__main__":
    # Define Input file path
    input_file_path = (
        "../Inputs/Generic_Prompts/Prompt_Set_1_EN.txt"  # File with one prompt per line
    )

    # Define output file paths for the respective models
    output_file_path_gpt = "../Results/LLM_Output/GPT/GPT_Results.json"  # File to save GPT results
    output_file_path_gemini = "../Results/LLM_Output/Gemini/Gemini_Results.json"  # File to save Gemini results
    output_file_path_mistral = "../Results/LLM_Output/Mistral/Mistral_Results.json"  # File to save Mistral results

    # Number of times to repeat the processing for each prompt
    repeat_count = 150

    # Function to process each model's prompts with logging messages
    def run_processes():
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # Function to add start/finish messages
            def log_and_run(func, input_file, output_file, repeat_times, model_name):
                print(f"Starting {model_name} processing...")
                func(input_file, output_file, repeat_times)
                print(f"Finished {model_name} processing.")

            # Submit each process to be run in parallel with log messages
            futures = [
                executor.submit(
                    log_and_run,
                    process_gpt_prompts,
                    input_file_path,
                    output_file_path_gpt,
                    repeat_count,
                    "GPT",
                ),
                executor.submit(
                    log_and_run,
                    process_gemini_prompts,
                    input_file_path,
                    output_file_path_gemini,
                    repeat_count,
                    "Gemini",
                ),
                executor.submit(
                    log_and_run,
                    process_mistral_prompts,
                    input_file_path,
                    output_file_path_mistral,
                    repeat_count,
                    "Mistral",
                ),
            ]

            # Wait for all processes to complete
            for future in concurrent.futures.as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    print(f"Error occurred during processing: {e}")

    # Run the processes
    run_processes()
