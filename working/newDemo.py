data = [
    {"Name": "Alice", "Age": 30, "Country": "USA"},
    {"Name": "Bob", "Age": 25, "Country": "UK"},
    {"Name": "Charlie", "Age": 35, "Country": "Canada"}
]

from openpyxl import Workbook

# Create a workbook and select active worksheet
wb = Workbook()
ws = wb.active
ws.title = "Fetched Data"

# Write headers
headers = list(data[0].keys())
ws.append(headers)

# Write data rows
for row in data:
    ws.append(list(row.values()))

# Save the file
wb.save("output.xlsx")

