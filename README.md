# 📦 Data Pipeline: SQL Server to SFTP (CSV Export)

## 📌 Overview

This project implements a modular and scalable **data engineering pipeline** that extracts data from a SQL Server database, serializes it into a CSV file, and transfers the file to a remote server via SFTP.

The solution follows a clean **ETL (Extract → Transform → Load)** architecture with a strong emphasis on:

- Streaming data processing (memory-efficient)
- Separation of concerns
- Fault tolerance (retry mechanisms)
- Production-oriented design principles

---

## 🏗️ Architecture

```text
SQL Server → Extractor → Serializer (CSV) → Local File → SFTP Loader → Remote Server
```

### Components

| Layer         | Module       | Responsibility                                           |
| ------------- | ------------ | -------------------------------------------------------- |
| Extract       | `extractor`  | Query SQL Server and stream data row-by-row              |
| Transform     | (implicit)   | Lightweight normalization (handled during serialization) |
| Load (local)  | `serializer` | Write data to CSV using streaming                        |
| Load (remote) | `loader`     | Upload file to SFTP server with retry logic              |
| Orchestration | `main.py`    | Coordinate the full pipeline                             |

---

## ⚙️ Key Features

### ✅ Streaming Data Processing

- Avoids loading entire datasets into memory
- Uses Python generators (`yield`) for efficient row-by-row processing

### ✅ Modular Design

- Each component has a single responsibility
- Easily extensible and testable

### ✅ Fault Tolerance

- Retry mechanism for SFTP uploads
- Safe file writing using temporary files

### ✅ Configuration Management

- Environment variables handled via `.env`
- No hardcoded credentials

### ✅ Data Partitioning

- Large datasets are split into multiple CSV files based on a configurable row limit

- Output files follow the pattern:

`data_part1.csv, data_part2.csv, ...`

- Each file includes headers and is independently consumable

---

## 🧰 Development Tools

### 📦 Dependency Management (`uv`)

This project uses **uv** for fast and reliable dependency management.

Key benefits:

- Extremely fast package installation and resolution
- Built-in virtual environment management
- Deterministic dependency handling

Typical workflow:

```bash
uv venv
uv pip install -r requirements.txt
```

---

### 🧹 Code Quality (`ruff`)

Code quality and formatting are enforced using **ruff**, a high-performance Python linter and formatter.

Key benefits:

- Fast linting (Rust-based)
- Combines multiple tools (flake8, isort, etc.)
- Enforces consistent code style

Common commands:

```bash
ruff check .
ruff format .
```

---

These tools ensure that the project maintains:

- Clean, readable, and consistent code
- Efficient dependency management
- Professional development standards suitable for production environments

---

## 📁 Project Structure

```text
project/
│
├── src/
│   ├── extractor/
│   │   └── extractor.py
│   │
│   ├── serializer/
│   │   └── csv_serializer.py
│   │
│   ├── loader/
│   │   └── sftp_loader.py
│   │
│   ├── output/     # Save CSV files
│   │
│   └── config/
│
├── tests/
├── main.py                # Pipeline orchestrator
├── .env                   # Environment variables
└── README.md
```

---

## 🔄 Pipeline Flow

1. **Extract**
   - Use database AdventureWorks2019
   - Connects to SQL Server using `pyodbc`
   - Executes a query against a view/table
   - Streams results as dictionaries

2. **Serialize**
   - Receives generator input
   - Writes CSV files in chunks using a row-based partitioning strategy
   - Generates multiple files `(*_partN.csv)` for large datasets
   - Uses temporary file to ensure atomic writes

3. **Load (SFTP)**
   - Connects via `paramiko`
   - Automatically discovers partitioned files in the output directory
   - Uploads file with retry logic
   - Handles connection failures gracefully

---

## 🔐 Configuration

All sensitive configuration is managed via environment variables:

```env
# Database
DB_SERVER=
DB_NAME=
DB_USER=
DB_PASS=
DB_DRIVER=

# SFTP
SFTP_SERVER=
SFTP_USER=
SFTP_PASS=
SFTP_PORT=22
```

---

## ▶️ Execution

Run the pipeline using:

```bash
python main.py
```

---

## 📊 Example Output

- Local file generated:

```text
output/data_YYYYMMDD_HHMMSS_part1.csv
output/data_YYYYMMDD_HHMMSS_part2.csv
output/data_YYYYMMDD_HHMMSS_part3.csv
```

- Uploaded to:

```text
/data_YYYYMMDD_HHMMSS_part1.csv
/data_YYYYMMDD_HHMMSS_part2.csv
/data_YYYYMMDD_HHMMSS_part3.csv
```

---

## 🧠 Design Decisions

### Streaming over Batch Processing

Avoids memory bottlenecks and enables scalability for large datasets.

### Temporary File Strategy

Prevents incomplete or corrupted files in case of failure during write operations.

### Retry Logic in SFTP

Improves robustness against transient network issues.

### Decoupled Components

Each module can be independently tested, reused, or replaced.

### Data Partitioning Strategy

Improve scalability for large datasets, avoiding large single-file transfers.

### Automated File Discovery

Eliminate manual file handling and simplify pipeline orchestration.

---

## 🚀 Future Improvements

- Add structured logging (`logging` module)
- Implement orchestration with Airflow or Prefect
- Support incremental loads (e.g., based on timestamps)
- Add file validation (checksum / row count verification)
- Support SSH key authentication for SFTP
- Containerization with Docker
- Adding test for modules

---

## 📚 Tech Stack

- Python 3.x
- `pyodbc` (SQL Server connectivity)
- `csv` (native serialization)
- `paramiko` (SFTP client)
- `python-dotenv` (configuration management)

---

## 👨‍💻 Author

This project was developed as part of a hands-on of current job project in **Data Engineering**, focusing on building production-oriented pipelines with best practices.

---

## 📌 Notes

This implementation prioritizes:

- Clarity over abstraction
- Learning over premature optimization
- Real-world engineering practices

---

## ⭐ Summary

This project demonstrates the ability to design and implement a **robust, modular, and scalable data pipeline**, suitable as a foundation for more advanced data engineering workflows.
