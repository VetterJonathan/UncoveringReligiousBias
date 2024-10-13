import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats

# Categories for the bar chart (models)
categories = ["Gemini 1.5 Flash", "GPT-4o mini", "Mistral NeMo"]

# Sample sizes for each prompt
sample_sizes = [900, 900, 900, 900, 2250, 900, 750, 750]

# Data for the number of responses (Gemini 1.5 Flash, GPT-4o mini, Mistral NeMo) for Prompt 1-8
Prompt_Answered = [
    [152, 900, 884],
    [388, 898, 886],
    [379, 899, 852],
    [591, 899, 871],
    [382, 2250, 2250],
    [828, 900, 900],
    [744, 750, 750],
    [749, 750, 750],
]

Prompt_Disclaimer = [
    [573, 0, 16],
    [191, 0, 14],
    [153, 0, 48],
    [286, 1, 0],
    [87, 0, 0],
    [70, 0, 0],
    [0, 0, 0],
    [1, 0, 0],
]

Prompt_Not_Answered = [
    [175, 0, 0],
    [321, 2, 0],
    [368, 1, 0],
    [23, 0, 29],
    [1781, 0, 0],
    [2, 0, 0],
    [6, 0, 0],
    [0, 0, 0],
]


def normalize(data, sample_size):
    """
    Normalize the data based on the sample size.

    :param data: List of raw counts to be normalized.
    :param sample_size: Total sample size used for normalization.
    :return: List of normalized proportions.
    """
    return [x / sample_size for x in data]


def calculate_confidence_intervals(proportions, sample_size, confidence_level=0.90):
    """
    Calculate the confidence intervals for the given proportions.

    :param proportions: List of proportions for which to calculate the confidence intervals.
    :param sample_size: The sample size used to calculate standard error.
    :param confidence_level: The confidence level for the interval (default is 0.90).
    :return: List of margin of errors for the confidence intervals.
    """
    z_score = stats.norm.ppf(1 - (1 - confidence_level) / 2)
    confidence_intervals = []
    for proportion in proportions:
        se = np.sqrt(proportion * (1 - proportion) / sample_size)  # Standard error
        margin_of_error = z_score * se
        confidence_intervals.append(margin_of_error)
    return confidence_intervals


def create_stacked_barchart(file_path):
    """
    Main function to normalize data, calculate confidence intervals, and plot the results.

    :param file_path: Path to save the generated plot.
    """
    # Lists to hold normalized data and confidence intervals for each prompt
    normalized_answered = []
    normalized_disclaimer = []
    normalized_not_answered = []

    ci_answered = []
    ci_disclaimer = []
    ci_not_answered = []

    # Normalize data and calculate confidence intervals for each prompt
    for i in range(8):
        norm_answered = normalize(Prompt_Answered[i], sample_sizes[i])
        norm_disclaimer = normalize(Prompt_Disclaimer[i], sample_sizes[i])
        norm_not_answered = normalize(Prompt_Not_Answered[i], sample_sizes[i])

        normalized_answered.append(norm_answered)
        normalized_disclaimer.append(norm_disclaimer)
        normalized_not_answered.append(norm_not_answered)

        # Calculate confidence intervals for each response type
        ci_answered.append(
            calculate_confidence_intervals(norm_answered, sample_sizes[i])
        )
        ci_disclaimer.append(
            calculate_confidence_intervals(norm_disclaimer, sample_sizes[i])
        )
        ci_not_answered.append(
            calculate_confidence_intervals(norm_not_answered, sample_sizes[i])
        )

    # Create the bar chart
    fig, ax = plt.subplots(figsize=(15, 8), dpi=150)
    bar_width = 0.1  # Width of each bar
    index = np.arange(len(categories))  # X-axis positions for the categories

    # Plot bars for each prompt with confidence intervals
    for i, (
        answered,
        disclaimer,
        not_answered,
        ci_ans,
        ci_disc,
        ci_not_ans,
    ) in enumerate(
        zip(
            normalized_answered,
            normalized_disclaimer,
            normalized_not_answered,
            ci_answered,
            ci_disclaimer,
            ci_not_answered,
        )
    ):

        offset = i * (
            bar_width + 0.01
        )  # Calculate offset for the bars to avoid overlap

        # Plot the 'Answered' bars with confidence intervals
        ax.bar(
            index + offset,
            answered,
            bar_width,
            color="g",
            alpha=0.7,
            yerr=ci_ans,
            capsize=3,
        )
        # Plot the 'Disclaimer' bars, stacked on top of 'Answered', with confidence intervals
        ax.bar(
            index + offset,
            disclaimer,
            bar_width,
            color="b",
            alpha=0.7,
            bottom=answered,
            yerr=ci_disc,
            capsize=3,
        )
        # Plot the 'Not Answered' bars, stacked on top of 'Answered' and 'Disclaimer', with confidence intervals
        ax.bar(
            index + offset,
            not_answered,
            bar_width,
            color="r",
            alpha=0.7,
            bottom=np.array(answered) + np.array(disclaimer),
            yerr=ci_not_ans,
            capsize=3,
        )

        # Add labels (Prompt 1-8) to each set of bars for clarity
        for j in range(len(categories)):
            ax.text(
                float(index[j]) + offset,
                0.02,
                f"Prompt {i + 1}",
                ha="center",  # Center the text on the bars
                va="bottom",  # Place text just above the baseline
                rotation=90,
            )  # Rotate text vertically for better fit

    # Set the x-axis label, y-axis label, and chart title
    ax.set_xlabel("Models")
    ax.set_ylabel("Proportion")
    ax.set_title(
        "Normalized Stacked Bar Chart of Responses by Prompt with 90% Confidence Intervals"
    )
    # Set the x-tick positions and labels
    ax.set_xticks(index + 3.5 * (bar_width + 0.01))  # Adjust for all prompts
    ax.set_xticklabels(categories)

    # Add a custom legend for the 'Answered', 'Disclaimer', and 'Not Answered' categories
    handles = [
        plt.Rectangle((0, 0), 1, 1, color="g", alpha=0.7),
        plt.Rectangle((0, 0), 1, 1, color="b", alpha=0.7),
        plt.Rectangle((0, 0), 1, 1, color="r", alpha=0.7),
    ]
    labels = ["Answered", "Disclaimer", "Not Answered"]
    ax.legend(handles, labels, loc="center right")

    # Save the chart to the specified path with high resolution (900 dpi)
    plt.savefig(file_path, dpi=900, bbox_inches="tight")

    # Show the chart
    plt.show()


if __name__ == "__main__":
    output_path = "../../Data/Graphs/answer_categories_stacked_barchart.png"  # Update this path as needed
    create_stacked_barchart(output_path)
