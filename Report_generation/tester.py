import matplotlib.pyplot as plt
from io import BytesIO


def plot_line_graph():
    # Sample data
    x = range(12)
    y = [5, 8, 3, 9, 1, 4, 7, 2, 6, 5, 3, 8]

    # Create a figure and axis object with black background
    fig, ax = plt.subplots(facecolor='black')

    # Plot the line graph with white line color
    ax.plot(x, y, color='black')

    # Set the facecolor of the axes to grey
    ax.set_facecolor('lightgrey')

    # Set the x-axis label
    ax.set_xlabel('X-axis', color='white')

    # Set the y-axis label
    ax.set_ylabel('Y-axis', color='white')

    # Set the title
    ax.set_title('title', color='white')

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

# Call the line graph function and get the image buffer
image_buffer = plot_line_graph()

# Show the image
plt.imshow(plt.imread(image_buffer))
plt.axis('off')
plt.show()
