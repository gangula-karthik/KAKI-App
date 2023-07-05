import matplotlib.pyplot as plt
import io
import base64


def plot_line_graph():
    # Define the x and y values for the data points
    months = ['January', 'February', 'March', 'April', 'May', 'June',
              'July', 'August', 'September', 'October', 'November', 'December']
    quantities = [10, 15, 12, 18, 20, 25, 22, 28, 30, 35, 32, 38]

    # Create the line graph
    plt.plot(months, quantities, marker='o', linestyle='-', color='blue')

    # Add labels and title
    plt.xlabel('Months')
    plt.ylabel('Quantity')
    plt.title('Monthly Quantity')

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




def plot_pie_chart():
    # Define the labels and sizes for the pie slices
    labels = ['Label 1', 'Label 2', 'Label 3', 'Label 4']
    sizes = [25, 35, 20, 20]

    # Create the pie chart
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)

    # Add a title
    plt.title('Pie Chart')

    # Convert the chart to a base64-encoded string
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    buffer.close()

    # Generate the HTML code for embedding the chart in a website
    html_code = f'<img src="data:image/png;base64,{image_base64}" alt="Pie Chart">'

    # Return the HTML code
    return html_code


