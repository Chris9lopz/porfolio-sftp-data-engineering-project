import json
import os
from datetime import datetime

from src.extractor.extractor import extract_data
from src.serializer.csv_serializer import write_to_csv_chunks
from src.loader.sftp_loader import upload_partitioned_files

CONFIG_PATH = "src/config/job_titles.json"


def main():
    try:
        # Ensure file output
        output_dir = "output"
        os.makedirs(output_dir, exist_ok=True)

        # Load job title mapping
        with open(CONFIG_PATH, encoding="utf-8") as f:
            job_titles: list[dict[str, str]] = json.load(f)

        for entry in job_titles:
            for job_id, job_name in entry.items():
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                safe_name = job_name.replace(" ", "_")
                base_name = f"data_{safe_name}_{timestamp}.csv"
                local_path = os.path.join(output_dir, base_name)

                print(f"\n--- Processing: {job_name} (ID: {job_id}) ---")

                # Extract
                data = extract_data(job_title=job_name)

                # Serialize to partitioned CSV files
                write_to_csv_chunks(data, local_path)

                # Upload all partitioned files to SFTP
                upload_partitioned_files(output_dir, "/")

                # Clean up local files after upload
                for fname in os.listdir(output_dir):
                    fpath = os.path.join(output_dir, fname)
                    try:
                        os.remove(fpath)
                    except OSError as e:
                        print(f"Error removing {fpath}: {e}")

        print("\nPipeline ejecutado correctamente.")

    except Exception as e:
        print(f"Error en el pipeline: {e}")
        raise


if __name__ == "__main__":
    main()
