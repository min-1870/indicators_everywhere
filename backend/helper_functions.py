import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
import os
from constants import PATH_TO_GRAPHS, S3_GRAPHS_PATH, S3_BUCKET_NAME, EC2_GRAPHS_PATH

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

def plot_two_graphs(stock_symbol, indicator_symbol, window, target_stock_data, column_1, label_1, column_2, label_2):
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

    # Add legend outside the plot
    fig.legend(loc="upper right", bbox_to_anchor=(1,1), bbox_transform=ax1.transAxes)

    # Add grid
    # ax1.grid(True)
    # plt.box(False)

    # Save the graph
    file_name = f'{stock_symbol}_{indicator_symbol}_{window}_{target_stock_data.index[-1].strftime("%Y-%m-%d")}.png'
    graphs_directory = f'{EC2_GRAPHS_PATH}{file_name}'
    plt.savefig(graphs_directory)
    upload_image_to_s3(file_name)

    plt.close()

def plot_graph(stock_symbol, indicator_symbol, window, target_stock_data, ylabel, columns):

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

    # Add legend outside the plot
    fig.legend(loc="upper right", bbox_to_anchor=(1,1), bbox_transform=ax.transAxes)

    # Adjust layout to make room for the legend
    plt.tight_layout()

    # Adding grid
    # ax.grid(True)
    # plt.box(False)

    # Save the graph 
    file_name = f'{stock_symbol}_{indicator_symbol}_{window}_{target_stock_data.index[-1].strftime("%Y-%m-%d")}.png'
    graphs_directory = f'{EC2_GRAPHS_PATH}{file_name}'
    plt.savefig(graphs_directory)
    upload_image_to_s3(file_name)

    plt.close()

def upload_image_to_s3(file_name):
    
    try:
        # Initialize the S3 client
        s3 = boto3.client('s3')

        local_directory = f"{PATH_TO_GRAPHS}{file_name}"
        s3_directory = f"{S3_GRAPHS_PATH}{file_name}"

        # Upload the file
        s3.upload_file(
            local_directory, 
            S3_BUCKET_NAME, 
            s3_directory,
            ExtraArgs={
                'ContentType': 'image/png',  
                'ACL': 'public-read'
            }
        )
    
    except FileNotFoundError:
        print("The file was not found.")
    except NoCredentialsError:
        print("Credentials not available.")
    except PartialCredentialsError:
        print("Incomplete credentials provided.")
    except Exception as e:
        print(f"An error occurred: {e}")