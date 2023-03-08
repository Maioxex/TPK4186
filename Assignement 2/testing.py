import pandas as pd

# Create a dataframe with some data
data = {'Name': ['John', 'Alice', 'Bob', 'Emma'],
        'Age': [25, 32, 18, 27],
        'City': ['Oslo', 'London', 'New York', 'Paris']}
df = pd.DataFrame(data)

# Export the dataframe to an Excel file
df.to_excel('data.xlsx', index=False)
