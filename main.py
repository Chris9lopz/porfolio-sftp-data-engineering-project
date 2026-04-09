import os
from datetime import datetime

from src.extractor.extractor import extract_data
from src.loader.sftp_loader import sftp_load_file
from src.serializer.csv_serializer import write_to_csv


def main():
    try:
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"data_{timestamp}.csv"
        local_path = os.path.join("output", file_name)

        data = extract_data()

        write_to_csv(data, local_path)

        remote_path = f"/{file_name}"
        sftp_load_file(local_path, remote_path)

        print("Pipeline ejecutado correctamente.")

    except Exception as e:
        print(f"Error en el pipeline: {e}")
        raise


if __name__ == "__main__":
    main()
