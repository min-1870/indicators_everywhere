import matplotlib.pyplot as plt
import matplotlib.font_manager as fm


# Load a custom font
# plt.rcParams['font.family'] = 'custom_font'
# plt.rcParams['font.path'] = ['/path/to/your/font.ttf']
plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Helvetica', 'Arial', 'DejaVu Sans'],
    'font.size': 10,
    'axes.labelsize': 10,
    'axes.titlesize': 12,
    'xtick.labelsize': 8,
    'ytick.labelsize': 8
})

def plot_two_graphs(indicator_symbol, window, target_stock_data, column_1, label_1, column_2, label_2):
    # Plotting
    fig, ax1 = plt.subplots(figsize=(12, 6))

    # Plot OBV
    ax1.plot(target_stock_data.index, target_stock_data[column_1], color='red', label=label_1)
    ax1.set_xlabel(label_1)
    ax1.set_ylabel('OBV', color='red')
    ax1.tick_params(axis='y', labelcolor='red')

    # Create a secondary y-axis for price
    ax2 = ax1.twinx()
    ax2.plot(target_stock_data.index, target_stock_data[column_2], color='blue', label=label_2)
    ax2.set_ylabel(label_2, color='blue')
    ax2.tick_params(axis='y', labelcolor='blue')

    # Adding title and legend
    fig.legend(loc="upper right", bbox_to_anchor=(1,1), bbox_transform=ax1.transAxes)

    # Add grid
    # ax1.grid(True)
    plt.box(False)
    # Save the graph
    plt.savefig(f'graphs/{indicator_symbol}_{window}_{target_stock_data.index[-1].strftime("%Y-%m-%d")}.png')
    plt.close()

def plot_graph(indicator_symbol, window, target_stock_data, ylabel, columns):

    # Create a new figure and axis
    fig, ax = plt.subplots(figsize=(12, 6))
        
    # Plot the Main graph
    for column in columns:
        ax.plot(
            target_stock_data.index,
            target_stock_data[column['column']],
            linestyle=column['linestyle'],
            color=column['color'],
            label=column['label']
        )

    # Adding labels
    ax.set_xlabel('Date')
    ax.set_ylabel(ylabel)

    # Adding grid
    # ax.grid(True)
    plt.box(False)
    # Add legend outside the plot
    fig.legend(loc="upper right", bbox_to_anchor=(1,1), bbox_transform=ax.transAxes)

    # Adjust layout to make room for the legend
    plt.tight_layout()

    # Save the graph
    plt.savefig(f'graphs/{indicator_symbol}_{window}_{target_stock_data.index[-1].strftime("%Y-%m-%d")}.png')
    plt.close()
