import matplotlib.pyplot as plt
from io import BytesIO
import base64


def plot_line_graph(month, quantity,title):


    # Define the x and y values for the data points
    months = month
    quantities = quantity

    fig, ax = plt.subplots()

    # Create the line graph
    plt.plot(months, quantities, marker='o', linestyle='-', color='white')


    ax.spines['bottom'].set_color('#17181C')  # Set color for the x-axis line
    ax.spines['right'].set_color('#17181C')  # Make the y-axis line invisible


    # Add labels and title
    plt.xlabel('Months', color = 'white')
    plt.ylabel('Quantity', color = 'white')
    plt.title(title)

    # Convert the graph to a base64-encoded string
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    buffer.close()

    # Generate the HTML code for embedding the graph in a website
    html_code = f'<img src="data:image/png;base64,{image_base64}" alt="Line Graph">'

    # Return the HTML code
    return html_code




def create_pie_chart_with_legend():
    # Sample data
    sizes = [30, 20, 15, 10, 25]
    labels = ['A', 'B', 'C', 'D', 'E']
    colors = ['#FF0000', '#00FF00', '#0000FF', '#FFFF00', '#00FFFF']

    # Create a figure and axis object
    fig, ax = plt.subplots()

    # Plot the pie chart
    wedges, _ = ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%')

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


