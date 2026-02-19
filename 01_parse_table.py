#!/usr/bin/env python3
import csv
import re
from bs4 import BeautifulSoup

with open('/Users/jstajich/.local/share/opencode/tool-output/tool_c740fc100001xn54RmfWbPk2k0', 'r') as f:
    html_content = f.read()

soup = BeautifulSoup(html_content, 'lxml')
table = soup.find('table')

# Get header rows
header_rows = table.find('thead').find_all('tr')
row1 = [cell.get_text(strip=True) for cell in header_rows[0].find_all(['th', 'td'])]
row2 = [cell.get_text(strip=True) for cell in header_rows[1].find_all(['th', 'td'])]

# Headers: first 6 from row1, then the 5 GenBank columns from row2
final_headers = row1[:6] + row2[6:]
# Clean up header names (remove footnote markers like 1, 2)
final_headers = [re.sub(r'\d+$', '', h).strip() for h in final_headers]

# Get data rows from tbody
data_rows = []
tbody = table.find('tbody')
if tbody:
    for tr in tbody.find_all('tr'):
        cells = [c.get_text(strip=True) for c in tr.find_all(['td', 'th'])]
        if cells and any(cells):
            data_rows.append(cells)

# Write to CSV
output_file = 'table1.csv'
with open(output_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(final_headers)
    for row in data_rows:
        writer.writerow(row)

print(f"CSV saved to {output_file}")
print(f"Total data rows: {len(data_rows)}")
print(f"Columns: {len(final_headers)}")
print("\nHeaders:", final_headers)
print("\nFirst 5 data rows:")
for row in data_rows[:5]:
    print(row)
