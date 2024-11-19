import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
import os
from pathlib import Path

from constants import S3_GRAPHS_PATH, S3_BUCKET_NAME, LOCAL_GRAPHS_PATH, PLOT_GRID, PLOT_BOX, S3_URL_TO_GRAPHS

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

def plot_two_graphs(stock_symbol, indicator_symbol, window, target_stock_data, column1, column2):
    # Plotting
    fig, ax1 = plt.subplots(figsize=(12, 6))

    # Plot OBV
    ax1.plot(
        target_stock_data.index,
        target_stock_data[column1['column']],
        color=column1['color'], label=column1['label'],
        linestyle=column1['linestyle']
    )
    ax1.set_xlabel('Date')
    ax1.set_ylabel(column1['label'])
    ax1.tick_params(axis='y', labelcolor=column1['color'])

    # Create a secondary y-axis for price
    ax2 = ax1.twinx()
    ax2.plot(
        target_stock_data.index,
        target_stock_data[column2['column']],
        color=column2['color'], label=column2['label'],
        linestyle=column2['linestyle']
    )
    ax2.set_xlabel('Date')
    ax2.set_ylabel(column2['label'])
    ax2.tick_params(axis='y', labelcolor=column2['color'])    

    # Customize graph style
    fig.legend(loc="upper right", bbox_to_anchor=(1,1), bbox_transform=ax1.transAxes)
    plt.tight_layout()
    ax1.grid(PLOT_GRID)
    for spine in ax1.spines.values():
        spine.set_visible(PLOT_BOX)
    for spine in ax2.spines.values():
        spine.set_visible(PLOT_BOX)
    
    # Get the directory of the graphs folder
    script_directory = Path(__file__).parent
    graphs_directory = script_directory / LOCAL_GRAPHS_PATH

    file_name = f'{stock_symbol}_{indicator_symbol}_{window}_{target_stock_data.index[-1].strftime("%Y-%m-%d")}.png'
    graphs_directory.mkdir(parents=True, exist_ok=True) # Construct folder
    plt.savefig(graphs_directory / file_name) # Save the graph image to the folder
    upload_image_to_s3(graphs_directory, file_name) # Upload the image to the s3

    plt.close()

    return f'{S3_URL_TO_GRAPHS}{file_name}'

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
    ax.set_xlabel('Date')
    ax.set_ylabel(ylabel)

    # Customize graph style
    fig.legend(loc="upper right", bbox_to_anchor=(1,1), bbox_transform=ax.transAxes)
    plt.tight_layout()
    ax.grid(PLOT_GRID)
    for spine in ax.spines.values():
        spine.set_visible(PLOT_BOX)
    
    # Get the directory of the graphs folder
    script_directory = Path(__file__).parent
    graphs_directory = script_directory / LOCAL_GRAPHS_PATH

    file_name = f'{stock_symbol}_{indicator_symbol}_{window}_{target_stock_data.index[-1].strftime("%Y-%m-%d")}.png'
    graphs_directory.mkdir(parents=True, exist_ok=True) # Construct folder
    plt.savefig(graphs_directory / file_name) # Save the graph image to the folder
    upload_image_to_s3(graphs_directory, file_name) # Upload the image to the s3

    plt.close()

    return f'{S3_URL_TO_GRAPHS}{file_name}'

def upload_image_to_s3(graphs_directory, file_name):
    
    try:
        # Initialize the S3 client
        s3 = boto3.client('s3')

        local_directory = graphs_directory / file_name
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

        
        if local_directory.exists():
            local_directory.unlink()
    
    except FileNotFoundError:
        print("The file was not found.")
    except NoCredentialsError:
        print("Credentials not available.")
    except PartialCredentialsError:
        print("Incomplete credentials provided.")
    except Exception as e:
        print(f"An error occurred: {e}")