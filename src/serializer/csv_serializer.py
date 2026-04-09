# Import modules
import csv
import os
import shutil


def write_to_csv(data, output_path):
    try:
        # Try to get first row
        first_row = next(data)
    except StopIteration:
        print("No data to write.")
        return

    # Identify first row
    fields = list(first_row.keys())
    # Set first as tmp file for performance
    temp_path = output_path + ".tmp"
    # Set counter for know amount of rows
    row_count = 0
    # Start writing process
    with open(temp_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        # Write the header
        writer.writeheader()
        # Write first_row generator
        writer.writerow(first_row)
        row_count += 1
        # Write for each row
        for row in data:
            writer.writerow(row)
            row_count += 1
    # Rename output file
    os.replace(temp_path, output_path)
    # Information about the process
    print(f"File Generated: {output_path} with {row_count} rows")
    # Move file
    shutil.move(output_path, os.path.join(
        'output', os.path.basename(output_path)))
