import matplotlib.pyplot as plt

# Define categories for the data
categories = ["Incorrectly Answered", "Not Enough Information", "Rejected"]

# Define the names of the models
prompts = ["Gemini 1.5 Flash", "GPT-4o mini", "Mistral NeMo"]

# Original data for the three systems
data = [
    [0, 103, 2573],  # Gemini
    [0, 0, 3],  # GPT
    [28, 0, 1],  # Mistral
]

# Define colors for the categories
colors = ["#4C9ED9", "#7EC8A2", "#E67A7A"]

# Calculate the total number of responses for each system
total_responses = [sum(system_data) for system_data in data]

# Normalize the data to represent them as percentages in the pie chart
normalized_data = [
    [(x / total) * 100 if total != 0 else 0 for x in system_data]
    for system_data, total in zip(data, total_responses)
]


# Function to adjust the percentage display
def autopct_func(p):
    """
    Adjust the percentage display for the pie chart.

    :param p: The percentage value
    :return: Formatted percentage string
    """
    return f"{p:.1f}%" if p > 0 else ""


def create_pie_chart(file_path):
    """
    Create and save a pie chart with the given data.

    :param file_path: The path where the pie chart will be saved
    """
    # Create a figure with 3 subplots arranged in a single row
    fig, axs = plt.subplots(1, 3, figsize=(18, 6))

    # Loop through each subplot and create a pie chart
    for i, ax in enumerate(axs):
        # Create the pie chart with normalized data and specified colors
        wedges, texts, autotexts = ax.pie(
            normalized_data[i], colors=colors, autopct=autopct_func, startangle=90
        )

        # Set the title for each subplot with the prompt name and total responses
        ax.set_title(f"{prompts[i]}\nTotal Responses: {total_responses[i]}")

        # Remove the default labels
        for text in texts:
            text.set_visible(False)

        # Increase the font size and make the percentage display bold
        for autotext in autotexts:
            autotext.set_fontsize(14)  # Set font size
            autotext.set_fontweight("bold")  # Set font weight to bold

        # Center the 100% label if present
        for j, p in enumerate(normalized_data[i]):
            if p == 100:
                # Move the existing text field to the center
                autotexts[j].set_position((0, 0))  # Adjust position

    # Add a legend outside the plots
    fig.legend(categories, loc="upper right", title="Categories", frameon=True)

    # Save the figure to a specified path
    plt.savefig(file_path, dpi=900, bbox_inches="tight")

    # Display the plot
    plt.show()


if __name__ == "__main__":
    output_path = "../../Data/Graphs/not_answered_pie_chart.png"  # Update this path as needed
    create_pie_chart(output_path)
