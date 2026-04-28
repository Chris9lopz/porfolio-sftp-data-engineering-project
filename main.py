import os
from datetime import datetime

from src.extractor.extractor import extract_data
from src.loader.sftp_loader import upload_partitioned_files
from src.serializer.csv_serializer import write_to_csv_chunks


def main():
    try:

        # Ensure file output
        output_dir = 'output'
        os.makedirs(output_dir, exist_ok=True)

        # Gemerate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"data_{timestamp}.csv"
        local_path = os.path.join("output", file_name)

        # Extract information
        data = extract_data()

        # Partitioned CSV files
        write_to_csv_chunks(data, local_path)

        # Upload all partitioned files to SFTP
        upload_partitioned_files(output_dir, '/')

        # Send status
        print("Pipeline ejecutado correctamente.")

    except Exception as e:
        print(f"Error en el pipeline: {e}")
        raise


if __name__ == "__main__":
    main()
