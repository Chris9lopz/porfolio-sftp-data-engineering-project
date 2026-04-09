# Import modules
import os

import pyodbc
from dotenv import load_dotenv

# Get .env variables
load_dotenv()


def extract_data():
    server = os.getenv('DB_SERVER')
    database = os.getenv('DB_NAME')
    username = os.getenv('DB_USER')
    password = os.getenv('DB_PASS')
    driver = os.getenv('DB_DRIVER')

    conn_str = (
        f"DRIVER={driver};"
        f"SERVER={server};"
        f"DATABASE={database};"
        f"UID={username};"
        f"PWD={password}"
    )

    query = """
        SELECT TOP (10) 
        [BusinessEntityID],
        [NationalIDNumber],
        [LoginID],
        [OrganizationLevel],
        [JobTitle],
        [BirthDate],
        [MaritalStatus],
        [Gender],
        [HireDate],
        [SalariedFlag],
        [VacationHours],
        [SickLeaveHours],
        [CurrentFlag],
        [ModifiedDate]
        FROM [AdventureWorks2019].[HumanResources].[Employee]
    """

    try:
        with pyodbc.connect(conn_str) as conn:
            cursor = conn.cursor()
            cursor.execute(query)

            columns = [column[0] for column in cursor.description]

            for row in cursor:
                yield dict(zip(columns, row, strict=True))

    except pyodbc.Error as e:
        print(f"Error al conectar: {e}")
        raise
