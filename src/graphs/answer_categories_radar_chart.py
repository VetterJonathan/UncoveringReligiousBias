import matplotlib.pyplot as plt
import numpy as np


def generate_radar_chart(categories, model_data, title, ax, max_value=750):
    """
    Generates a radar chart for a specific model and adds it to the provided subplot axis.

    :param categories: List of categories (e.g., religions) for the radar chart.
    :param model_data: A list containing the data for Answered, Disclaimer, and Not Answered responses.
    :param title: The title for the radar chart.
    :param ax: The axis on which to plot the radar chart.
    :param max_value: The maximum value for the y-axis (default is 750).
    """
    angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
    angles += angles[:1]  # Repeat the first angle to close the chart

    # Extend the data arrays to create a closed loop
    answered, disclaimer, not_answered = model_data
    answered += answered[:1]
    disclaimer += disclaimer[:1]
    not_answered += not_answered[:1]

    # Set the y-axis limits
    ax.set_ylim(0, max_value)

    # Plot and fill the radar chart
    ax.fill(angles, answered, color="g", alpha=0.25, label="Answered")
    ax.fill(angles, disclaimer, color="b", alpha=0.25, label="Disclaimer")
    ax.fill(angles, not_answered, color="r", alpha=0.25, label="Not Answered")

    # Draw lines for each category
    ax.plot(angles, answered, color="g", linewidth=2, linestyle="solid")
    ax.plot(angles, disclaimer, color="b", linewidth=2, linestyle="solid")
    ax.plot(angles, not_answered, color="r", linewidth=2, linestyle="solid")

    # Configure the x-axis
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories)

    # Set the title and legend
    ax.set_title(title, size=20, color="black", y=1.1)
    ax.legend(loc="upper right", bbox_to_anchor=(1.1, 1.1))


def plot_models_radar_chart(categories, model_data_dict, file_path):
    """
    Creates a radar chart for each model and saves the plot to a file.

    :param categories: List of categories (e.g., religions) for the radar charts.
    :param model_data_dict: A dictionary containing model names as keys and their respective data as values.
    :param file_path: The file path where the radar chart image will be saved.
    """
    fig, axs = plt.subplots(1, 3, figsize=(20, 8), subplot_kw=dict(polar=True))

    # Generate radar chart for each model
    generate_radar_chart(
        categories, model_data_dict["Gemini"], "Gemini 1.5 Flash", axs[0]
    )
    generate_radar_chart(categories, model_data_dict["GPT"], "GPT-4o mini", axs[1])
    generate_radar_chart(categories, model_data_dict["Mistral"], "Mistral NeMo", axs[2])

    # Adjust layout and save figure
    plt.tight_layout()
    plt.savefig(file_path, dpi=900, bbox_inches="tight")
    plt.show()


def create_graphic(file_path):
    """
    Main function to execute the radar chart generation process.

    :param file_path: The file path where the radar chart image will be saved.
    """
    # Categories for the radar chart (religions)
    categories = ["Christianity", "Islam", "Hinduism", "Judaism", "Buddhism", "Atheism"]

    # Data for the models (Answered, Disclaimer, Not Answered)
    model_data_dict = {
        "Gemini": [
            [516, 169, 320, 126, 749, 458],  # Answered
            [222, 323, 280, 156, 1, 291],  # Disclaimer
            [12, 258, 150, 468, 0, 1],  # Not Answered
        ],
        "GPT": [
            [750, 749, 750, 747, 750, 750],  # Answered
            [0, 0, 0, 1, 0, 0],  # Disclaimer
            [0, 1, 0, 2, 0, 0],  # Not Answered
        ],
        "Mistral": [
            [729, 736, 736, 703, 745, 744],  # Answered
            [5, 12, 12, 46, 1, 2],  # Disclaimer
            [16, 2, 2, 1, 4, 6],  # Not Answered
        ],
    }

    # Generate and save the radar chart
    plot_models_radar_chart(categories, model_data_dict, file_path)


if __name__ == "__main__":
    output_path = "../../Data/Graphs/answer_categories_radar_charts.png"  # Update this path as needed
    create_graphic(output_path)
