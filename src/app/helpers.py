import matplotlib.pyplot as plt
from pathlib import Path
from src.app.api import upload_image_to_s3
from src.app.constants import (
    LOCAL_GRAPHS_PATH,
    PLOT_GRID,
    PLOT_BOX,
    S3_URL_TO_GRAPHS,
    DEBUG
)

plt.rcParams.update(
    {
        "font.family": "sans-serif",
        "font.sans-serif": ["Helvetica", "Arial", "DejaVu Sans"],
        "font.size": 10,
        "axes.labelsize": 10,
        "axes.titlesize": 12,
        "xtick.labelsize": 8,
        "ytick.labelsize": 8,
    }
)


def plot_two_graphs(
    stock_symbol, indicator_symbol, window, target_stock_data, column1, column2
):
    # Plotting
    fig, ax1 = plt.subplots(figsize=(12, 6))

    # Create a y-axis
    ax1.plot(
        target_stock_data.index,
        target_stock_data[column1["column"]],
        color=column1["color"],
        label=column1["label"],
        linestyle=column1["linestyle"],
    )
    ax1.set_xlabel("Date")
    ax1.set_ylabel(column1["label"])
    ax1.tick_params(axis="y", labelcolor=column1["color"])

    # Create a secondary y-axis
    ax2 = ax1.twinx()
    ax2.plot(
        target_stock_data.index,
        target_stock_data[column2["column"]],
        color=column2["color"],
        label=column2["label"],
        linestyle=column2["linestyle"],
    )
    ax2.set_xlabel("Date")
    ax2.set_ylabel(column2["label"])
    ax2.tick_params(axis="y", labelcolor=column2["color"])

    # Customize graph style
    fig.legend(loc="upper right", bbox_to_anchor=(1, 1), bbox_transform=ax1.transAxes)
    plt.tight_layout()
    ax1.grid(PLOT_GRID)
    for spine in ax1.spines.values():
        spine.set_visible(PLOT_BOX)
    for spine in ax2.spines.values():
        spine.set_visible(PLOT_BOX)

    # Get the directory of the graphs folder
    script_directory = Path(__file__).parent
    graphs_directory = script_directory / LOCAL_GRAPHS_PATH

    file_name = (
        f"{stock_symbol}_"
        f"{indicator_symbol}_"
        f"{window}_"
        f"{target_stock_data.index[-1].strftime('%Y-%m-%d')}.png"
    )
    graphs_directory.mkdir(parents=True, exist_ok=True)  # Construct folder
    plt.savefig(graphs_directory / file_name)  # Save the graph image to the folder
    upload_image_to_s3(graphs_directory, file_name)  # Upload the image to the s3

    plt.close()

    if DEBUG:
        return f"{graphs_directory}/{file_name}"
    return f"{S3_URL_TO_GRAPHS}{file_name}"


def plot_graph(
    stock_symbol,
    indicator_symbol,
    window,
    target_stock_data,
    ylabel,
    columns,
    lines=False,
):

    # Create a new figure and axis
    fig, ax = plt.subplots(figsize=(12, 6))

    # Plot the Horizontal Lines
    if lines:
        for line in lines:
            ax.axhline(
                y=line["y"],
                linestyle=line["linestyle"],
                color=line["color"],
                label=line["label"],
            )

    # Plot the Main graph
    for column in columns:
        ax.plot(
            target_stock_data.index,
            target_stock_data[column["column"]],
            linestyle=column["linestyle"],
            color=column["color"],
            label=column["label"],
        )
    ax.set_xlabel("Date")
    ax.set_ylabel(ylabel)

    # Customize graph style
    fig.legend(loc="upper right", bbox_to_anchor=(1, 1), bbox_transform=ax.transAxes)
    plt.tight_layout()
    ax.grid(PLOT_GRID)
    for spine in ax.spines.values():
        spine.set_visible(PLOT_BOX)

    # Get the directory of the graphs folder
    script_directory = Path(__file__).parent
    graphs_directory = script_directory / LOCAL_GRAPHS_PATH

    file_name = (
        f"{stock_symbol}_"
        f"{indicator_symbol}_"
        f"{window}_"
        f"{target_stock_data.index[-1].strftime('%Y-%m-%d')}.png"
    )
    graphs_directory.mkdir(parents=True, exist_ok=True)  # Construct folder
    plt.savefig(graphs_directory / file_name)  # Save the graph image to the folder
    upload_image_to_s3(graphs_directory, file_name)  # Upload the image to the s3

    plt.close()

    if DEBUG:
        return f"{graphs_directory}/{file_name}"
    return f"{S3_URL_TO_GRAPHS}{file_name}"
