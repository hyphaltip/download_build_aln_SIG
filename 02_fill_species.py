#!/usr/bin/env python3
import csv

input_file = 'table1.csv'
output_file = 'table1_filled.csv'

with open(input_file, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    rows = list(reader)

# Fill in empty Species values with previous row's species
for i in range(1, len(rows)):
    if not rows[i][0].strip():
        rows[i][0] = rows[i-1][0]

with open(output_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerows(rows)

print(f"Output saved to {output_file}")
print(f"Total rows: {len(rows) - 1}")

# Show some examples
print("\nFirst 10 rows:")
for row in rows[:10]:
    print(row)
