import matplotlib.pyplot as plt
from io import BytesIO
from io import BytesIO
from PIL import Image

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

image_buffer = create_pie_chart_with_legend()



def show_image_from_buffer(buffer):
    # Open the image from the buffer
    image = Image.open(buffer)

    # Display the image
    plt.imshow(image)
    plt.axis('off')
    plt.show()

show_image_from_buffer(image_buffer)
