import matplotlib.pyplot as plt
from docx import Document
from docx.shared import Inches

# Generate some random data and plot it
x = [1, 2, 3, 4, 5]
y = [10, 8, 6, 4, 2]
plt.plot(x, y)
plt.savefig('my_plot.png')
# Create a new Word document
document = Document()

# Add a title to the document
document.add_heading('My Plot', level=0)

# Add the plot to the document
document.add_picture('my_plot.png', width=Inches(6))

# Save the document
document.save('my_document.docx')