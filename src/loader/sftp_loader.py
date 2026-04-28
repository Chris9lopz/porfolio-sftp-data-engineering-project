import glob
import os
import time

import paramiko
from dotenv import load_dotenv

load_dotenv()


def sftp_load_file(local_path, remote_path, max_retries=3, delay=5):
    for attempt in range(1, max_retries + 1):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            print(f"Intento {attempt} de {max_retries}")

            # Connection
            ssh.connect(
                hostname=os.getenv('SFTP_SERVER'),
                username=os.getenv('SFTP_USER'),
                password=os.getenv('SFTP_PASS'),
                port=int(os.getenv('SFTP_PORT', 22))
            )

            sftp = ssh.open_sftp()

            # Check file
            if not os.path.exists(local_path):
                raise FileNotFoundError(f"Archivo no encontrado: {local_path}")

            # Upload
            sftp.put(local_path, remote_path)

            print(f"Archivo subido correctamente a {remote_path}")

            # Close Connections
            sftp.close()
            ssh.close()

            return

        except Exception as e:
            print(f"Error en intento {attempt}: {e}")

            # Close Connections
            try:
                ssh.close()
            except Exception as e:
                pass

            if attempt < max_retries:
                print(f"Reintentando en {delay} segundos...")
                time.sleep(delay)
            else:
                print("Se alcanzó el máximo de reintentos.")
                raise


def upload_partitioned_files(local_dir, remote_dir):

    pattern = os.path.join(local_dir, '*_part*.csv')
    files = sorted(glob.glob(pattern))

    if not files:
        print('No files found to upload')
        return

    print(f'Total files found: {len(files)}')

    for file_path in files:
        file_name = os.path.basename(file_path)
        remote_path = f'{remote_dir}/{file_name}'

        print('File uploading...')

        try:
            sftp_load_file(file_path, remote_path)
        except Exception as e:
            print(f'Error uploading {file_name}: {e}')
