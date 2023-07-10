import matplotlib.pyplot as plt
from io import BytesIO
import base64
import io

def plot_line_graph(month, quantity,title):
    # Sample data
    x = month
    y = quantity

    # Create a figure and axis object with black background
    fig, ax = plt.subplots(facecolor='black')

    # Plot the line graph with white line color
    ax.plot(x, y, color='black')

    # Set the x-axis label
    ax.set_xlabel('X-axis', color='white')

    # Set the y-axis label
    ax.set_ylabel('Y-axis', color='white')

    # Set the title
    ax.set_title(title, color='white')

    # Set the color of the x-axis and y-axis lines
    ax.spines['bottom'].set_color('white')
    ax.spines['left'].set_color('white')

    # Set the color of the x-axis and y-axis labels
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')

    # Set the color of the title
    ax.title.set_color('white')

    # Set the color of the ticks on the x-axis and y-axis
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')

    # Save the plot to an in-memory buffer
    buffer = BytesIO()
    plt.savefig(buffer, format='png', facecolor=fig.get_facecolor(), bbox_inches='tight')
    buffer.seek(0)

    # Close the plot to free memory
    plt.close()

    # Return the image buffer
    return buffer




def create_pie_chart_with_legend():
    # Sample data
    sizes = [30, 20, 15, 10, 25]
    labels = ['A', 'B', 'C', 'D', 'E']
    colors = ['#FF0000', '#00FF00', '#0000FF', '#FFFF00', '#00FFFF']

    # Create a figure and axis object
    fig, ax = plt.subplots()

    # Plot the pie chart
    wedges, _ = ax.pie(sizes, labels=labels, colors=colors)

    # Equal aspect ratio ensures that pie is drawn as a circle
    ax.axis('equal')

    # Create a legend at the side
    ax.legend(wedges, labels, loc='center left', bbox_to_anchor=(1, 0.5))

    # Save the plot to an in-memory buffer
    buffer = BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')
    buffer.seek(0)

    # Close the plot to free memory
    plt.close()

    # Return the image buffer
    return buffer


