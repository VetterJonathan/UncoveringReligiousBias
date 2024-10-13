import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap

# Define the models to be analyzed
systems = ["GPT-4o mini", "Mistral NeMo", "Gemini 1.5 Flash", "Related Work"]

# Total cases for each religion (Hindus have NaN for "Related Work")
total_cases = {
    "Islam": [1800, 1800, 1800, 100],
    "Christianity": [1800, 1800, 1800, 100],
    "Judaism": [1800, 1800, 1800, 100],
    "Buddhism": [1800, 1800, 1800, 100],
    "Atheism": [1500, 1500, 1500, 100],
    "Hinduism": [1800, 1800, 1800, np.nan],  # NaN for "Related Work"
}

# Bias cases for each religion (Hindus have NaN for "Related Work")
bias_cases = {
    "Islam": [0, 0, 0, 66],
    "Christianity": [0, 0, 0, 15],
    "Judaism": [0, 2, 0, 8],
    "Buddhism": [0, 0, 0, 4],
    "Atheism": [0, 0, 3, 2],
    "Hinduism": [0, 0, 0, np.nan],  # NaN for "Related Work"
}


def calculate_percentage(bias, total):
    """
    Calculate the percentage of bias cases for each religion.

    :param bias: List of bias cases for each model.
    :param total: List of total cases for each model.
    :return: List of percentages of bias cases for each model.
    """
    percentages = []
    for b, t in zip(bias, total):
        if t > 0:
            percentages.append(b / t * 100)
        else:
            percentages.append(0)
    return percentages


def create_heatmap(file_path):
    """
    Create and save a heatmap representation of bias cases.

    :param file_path: The file path to save the heatmap image.
    """
    # Calculate the percentage of bias cases for each religion
    percent_bias = {}
    for religion in total_cases.keys():
        percent_bias[religion] = calculate_percentage(
            bias_cases[religion], total_cases[religion]
        )

    # Create heatmap data
    data = np.array(
        list(percent_bias.values())
    )  # Convert the percentage dictionary to a numpy array

    # Square root transformation of the data for better visualization
    data_transformed = np.sqrt(data)

    religion_labels = list(total_cases.keys())  # List of religions
    model_labels = systems  # List of models

    # Define a custom colormap from green to red
    colors = [
        "#00ff00",
        "#99cc00",
        "#ffff00",
        "#ffcc00",
        "#ff9900",
        "#ff0000",
    ]  # Green to Red colors
    cmap = LinearSegmentedColormap.from_list("custom_cmap", colors, N=256)

    # Set manual boundaries for color transitions
    boundaries = [0, 5, 10, 20, 30, 66]  # Adjust these as needed for the color ranges
    norm = plt.Normalize(
        vmin=0, vmax=np.sqrt(66)
    )  # Normalize the transformed values for coloring

    # Create a mask for the cell corresponding to "Related Work" x "Hindus"
    mask = np.zeros_like(data, dtype=bool)
    mask[-1, -1] = True  # Mask the last cell in the last row

    # Create the heatmap
    fig, ax = plt.subplots(figsize=(10, 6))
    heatmap = sns.heatmap(
        data_transformed,
        annot=data,
        fmt=".1f",
        cmap=cmap,
        xticklabels=model_labels,
        yticklabels=religion_labels,
        cbar_kws={"label": "Bias-Cases (%)", "ticks": boundaries},
        norm=norm,
        mask=mask,
    )

    # Adjust the color scale ticks
    cbar = heatmap.collections[0].colorbar
    cbar.set_ticks([np.sqrt(b) for b in boundaries])
    cbar.set_ticklabels(boundaries)

    # Change the text color in the heatmap cells
    for text in heatmap.texts:
        text.set_color("black")

    # Set labels and formatting
    ax.set_xlabel("Models")
    ax.set_ylabel("Religion")

    # Rotate the axis labels for better visibility
    plt.xticks(rotation=45)  # Rotate x-axis labels (models)
    plt.yticks(rotation=0)  # Keep y-axis labels (religions) horizontal

    plt.tight_layout()  # Adjust layout to fit labels and titles

    # Save the heatmap to a specified path with high resolution
    plt.savefig(file_path, dpi=900, bbox_inches="tight")

    # Display the heatmap
    plt.show()


if __name__ == "__main__":
    output_path = "../../Data/Graphs/bias_heatmap.png"  # Update this path as needed
    create_heatmap(output_path)
