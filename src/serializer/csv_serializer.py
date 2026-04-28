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


def write_to_csv_chunks(data, output_path, max_rows=90):
    try:
        # Try to get first row
        first_row = next(data)
    except StopIteration:
        print("No data to write.")
        return

    # Identify first row
    fields = list(first_row.keys())

    file_index = 1
    row_count_file = 0
    total_rows = 0

    def get_file_path(index):
        name, ext = os.path.splitext(output_path)
        return f"{name}_part{index}{ext}"

    current_file_path = get_file_path(file_index)
    temp_path = current_file_path + ".tmp"

    file = open(temp_path, 'w', newline='', encoding='utf-8')
    writer = csv.DictWriter(file, fieldnames=fields)
    writer.writeheader()

    writer.writerow(first_row)
    row_count_file += 1
    total_rows += 1

    for row in data:
        if row_count_file >= max_rows:
            file.close()
            os.replace(temp_path, current_file_path)

            print(
                f"File Generated: {current_file_path} with {row_count_file} rows")

            file_index += 1
            row_count_file = 0

            current_file_path = get_file_path(file_index)
            temp_path = current_file_path + ".tmp"

            file = open(temp_path, 'w', newline='', encoding='utf-8')
            writer = csv.DictWriter(file, fieldnames=fields)
            writer.writeheader()

        writer.writerow(row)
        row_count_file += 1
        total_rows += 1

    file.close()
    os.replace(temp_path, current_file_path)

    print(f"File Generated: {current_file_path} with {row_count_file} rows")
    print(f'Total files proccessed: {total_rows}')
