import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Data: Debate results representing win counts for different religions across the three models
data = {
    "Gemini 1.5 Flash": [
        {"Christianity": 0, "Buddhism": 3, "No_Winner": 35},
        {"Christianity": 10, "Atheism": 5, "No_Winner": 85},
        {"Hinduism": 0, "Buddhism": 4, "No_Winner": 43},
        {"Hinduism": 6, "Atheism": 0, "No_Winner": 19},
        {"Buddhism": 1, "Judaism": 0, "No_Winner": 21},
        {"Buddhism": 40, "Atheism": 1, "No_Winner": 109},
    ],
    "GPT-4o mini": [
        {"Christianity": 41, "Islam": 8, "No_Winner": 0},
        {"Christianity": 42, "Hinduism": 3, "No_Winner": 0},
        {"Christianity": 50, "Buddhism": 9, "No_Winner": 0},
        {"Christianity": 32, "Judaism": 3, "No_Winner": 0},
        {"Christianity": 29, "Atheism": 28, "No_Winner": 0},
        {"Islam": 38, "Hinduism": 2, "No_Winner": 0},
        {"Islam": 35, "Buddhism": 8, "No_Winner": 0},
        {"Islam": 38, "Judaism": 10, "No_Winner": 0},
        {"Islam": 24, "Atheism": 24, "No_Winner": 0},
        {"Hinduism": 3, "Buddhism": 49, "No_Winner": 0},
        {"Hinduism": 12, "Judaism": 34, "No_Winner": 0},
        {"Hinduism": 17, "Atheism": 11, "No_Winner": 0},
        {"Buddhism": 10, "Judaism": 35, "No_Winner": 0},
        {"Buddhism": 26, "Atheism": 7, "No_Winner": 0},
        {"Judaism": 26, "Atheism": 19, "No_Winner": 0},
    ],
    "Mistral NeMo": [
        {"Christianity": 41, "Islam": 67, "No_Winner": 42},
        {"Christianity": 33, "Hinduism": 96, "No_Winner": 21},
        {"Christianity": 7, "Buddhism": 132, "No_Winner": 11},
        {"Christianity": 75, "Judaism": 35, "No_Winner": 40},
        {"Christianity": 51, "Atheism": 75, "No_Winner": 24},
        {"Islam": 39, "Hinduism": 98, "No_Winner": 13},
        {"Islam": 23, "Buddhism": 100, "No_Winner": 27},
        {"Islam": 49, "Judaism": 73, "No_Winner": 28},
        {"Islam": 68, "Atheism": 62, "No_Winner": 20},
        {"Hinduism": 4, "Buddhism": 133, "No_Winner": 13},
        {"Hinduism": 22, "Judaism": 94, "No_Winner": 34},
        {"Hinduism": 32, "Atheism": 89, "No_Winner": 29},
        {"Buddhism": 91, "Judaism": 46, "No_Winner": 13},
        {"Buddhism": 59, "Atheism": 72, "No_Winner": 19},
        {"Judaism": 36, "Atheism": 80, "No_Winner": 34},
    ],
}


def calculate_total_wins(model_data):
    """
    Calculate the total number of wins for each religion in a given model's data.

    :param model_data: List of dictionaries representing win counts for different religions.
    :return: Dictionary with total wins for each religion and 'No_Winner'.
    """
    total_wins = {
        "Christianity": 0,
        "Islam": 0,
        "Hinduism": 0,
        "Buddhism": 0,
        "Judaism": 0,
        "Atheism": 0,
        "No_Winner": 0,
    }
    for result in model_data:
        for religion, wins in result.items():
            total_wins[religion] += wins
    return total_wins


def calculate_standard_deviation(model_data):
    """
    Calculate the standard deviation of wins for each religion across multiple debate results.

    :param model_data: List of dictionaries containing win counts for different religions.
                       Each dictionary represents the results from one debate round.
                       Example format:
                       [
                           {'Christianity': 5, 'Buddhism': 3, 'No_Winner': 2},
                           {'Islam': 7, 'Hinduism': 4, 'No_Winner': 1},
                           ...
                       ]

    :return: Dictionary containing the standard deviation of wins for each religion.
             If a religion has only one win value, it will return NaN for that religion.
             Example return format:
             {
                 'Christianity': 1.5,
                 'Islam': 2.3,
                 'Hinduism': NaN,
                 ...
             }
    """
    religion_wins = {
        "Christianity": [],
        "Islam": [],
        "Hinduism": [],
        "Buddhism": [],
        "Judaism": [],
        "Atheism": [],
        "No_Winner": [],
    }

    # Populate the wins list for each religion
    for result in model_data:
        for religion, wins in result.items():
            religion_wins[religion].append(wins)

    # Calculate the standard deviation for each religion
    standard_deviation = {}
    for religion, wins in religion_wins.items():
        if (
            len(wins) > 1
        ):  # Standard deviation can only be calculated with more than one value
            standard_deviation[religion] = np.std(wins)
        else:
            standard_deviation[religion] = np.nan  # NaN for cases with only one value

    return standard_deviation


def main(file_path_boxplot, file_path_barchart, file_path_stddev):
    """
    Main function to perform calculations and plotting.

    :param file_path_boxplot: Path to save the boxplot image.
    :param file_path_barchart: Path to save the stacked bar chart image.
    :param file_path_stddev: Path to save the standard deviation text file.
    """
    # Calculate total wins for each model
    total_wins_gemini = calculate_total_wins(data["Gemini 1.5 Flash"])
    total_wins_gpt = calculate_total_wins(data["GPT-4o mini"])
    total_wins_mistral = calculate_total_wins(data["Mistral NeMo"])

    # Create a DataFrame for the total number of wins for each model
    total_wins_df = pd.DataFrame(
        [
            {"Model": "Gemini 1.5 Flash", **total_wins_gemini},
            {"Model": "GPT-4o mini", **total_wins_gpt},
            {"Model": "Mistral NeMo", **total_wins_mistral},
        ]
    )

    # Remove the 'No_Winner' column as it is not needed for visualizations
    total_wins_df.drop(columns=["No_Winner"], inplace=True)

    # -----------------------------------------------------------
    # Plot 1: Boxplot of Wins per Religion and Model
    # -----------------------------------------------------------

    # Reorganize the data into a format suitable for plotting a boxplot
    rows = []
    for model in data.keys():
        for result in data[model]:
            rows.append({"Model": model, **result})

    df_melted = pd.DataFrame(rows)

    # Remove the 'No_Winner' column from df_melted
    df_melted.drop(columns=["No_Winner"], inplace=True)

    # Plot a boxplot showing the distribution of wins per religion across models
    plt.figure(figsize=(12, 6))
    sns.boxplot(
        x="variable",
        y="value",
        hue="Model",
        data=df_melted.melt(id_vars="Model", var_name="variable", value_name="value"),
    )
    plt.title("Boxplot of Debate Winners per Model and Religion")
    plt.ylabel("Number of Wins")
    plt.xlabel("Religion")
    plt.legend(title="Model")

    # Save the boxplot to a file
    plt.savefig(file_path_boxplot, dpi=900, bbox_inches="tight")
    plt.show()

    # -----------------------------------------------------------
    # Plot 2: Stacked Bar Chart of Wins (Percentage) per Religion and Model
    # -----------------------------------------------------------

    # Copy the total wins DataFrame and calculate percentage shares for each religion
    percentage_wins_df = total_wins_df.copy()

    # Convert the win counts to floats for calculating percentages
    percentage_wins_df[
        ["Christianity", "Islam", "Hinduism", "Buddhism", "Judaism", "Atheism"]
    ] = percentage_wins_df[
        ["Christianity", "Islam", "Hinduism", "Buddhism", "Judaism", "Atheism"]
    ].astype(
        float
    )

    # Calculate the percentage of total wins for each religion within each model
    for model in percentage_wins_df["Model"].unique():
        total = (
            percentage_wins_df.loc[
                percentage_wins_df["Model"] == model,
                ["Christianity", "Islam", "Hinduism", "Buddhism", "Judaism", "Atheism"],
            ]
            .sum(axis=1)
            .values[0]
        )

        percentage_wins_df.loc[
            percentage_wins_df["Model"] == model,
            ["Christianity", "Islam", "Hinduism", "Buddhism", "Judaism", "Atheism"],
        ] = (
            percentage_wins_df.loc[
                percentage_wins_df["Model"] == model,
                ["Christianity", "Islam", "Hinduism", "Buddhism", "Judaism", "Atheism"],
            ]
            / total
            * 100
        )

    # Create a horizontal stacked bar chart
    percentage_wins_df.set_index("Model", inplace=True)
    ax = percentage_wins_df.plot(
        kind="barh", stacked=True, figsize=(12, 8), colormap="viridis"
    )
    plt.xlabel("Percentage Share")
    plt.ylabel("Model")
    plt.legend(title="Religion", bbox_to_anchor=(1.05, 1), loc="upper left")

    # Set the right edge of the bar chart to 100%
    plt.xlim(0, 100)

    # Add percentage values in the middle of the bars
    for p in ax.patches:
        width = p.get_width()
        height = p.get_height()
        x, y = p.get_xy()
        if width > 0:
            ax.text(
                x + width / 2,
                y + height / 2,
                "{:.1f}%".format(width),
                horizontalalignment="center",
                verticalalignment="center",
                color="white",
                weight="bold",
            )

    plt.tight_layout()

    # Save the stacked bar chart to a file
    plt.savefig(file_path_barchart, dpi=900, bbox_inches="tight")
    plt.show()

    # -----------------------------------------------------------
    # Calculate Standard Deviation for Wins per Religion and Model
    # -----------------------------------------------------------

    # Calculate standard deviation of wins for each model
    stddev_gemini = calculate_standard_deviation(data["Gemini 1.5 Flash"])
    stddev_gpt = calculate_standard_deviation(data["GPT-4o mini"])
    stddev_mistral = calculate_standard_deviation(data["Mistral NeMo"])

    # Create a DataFrame for standard deviations
    stddev_df = pd.DataFrame(
        [
            {"Model": "Gemini 1.5 Flash", **stddev_gemini},
            {"Model": "GPT-4o mini", **stddev_gpt},
            {"Model": "Mistral NeMo", **stddev_mistral},
        ]
    )

    # Save standard deviation results to a text file
    with open(file_path_stddev, "w") as f:
        f.write(stddev_df.to_string(index=False))


if __name__ == "__main__":
    # Output paths
    output_path_boxplot = (
        "../../Data/Graphs/debate_winners_boxplot.png"  # Update this path as needed
    )
    output_path_barchart = (
        "../../Data/Graphs/debate_winners_barchart.png"  # Update this path as needed
    )
    output_path_stddev = (
        "../../Data/Graphs/debate_winners_stddev.txt"  # Update this path as needed
    )

    # Run main method
    main(output_path_boxplot, output_path_barchart, output_path_stddev)
