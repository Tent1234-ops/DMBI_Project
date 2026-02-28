import pandas as pd
import mysql.connector
from datetime import datetime


def log_metadata(file_path, zone, status):

    df = pd.read_csv(file_path)

    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="youtube_pipeline"
    )

    cursor = connection.cursor()

    insert_query = """
        INSERT INTO pipeline_metadata
        (zone, file_name, total_rows, total_columns, created_at, status)
        VALUES (%s, %s, %s, %s, %s, %s)
    """

    values = (
        zone,
        file_path,
        len(df),
        len(df.columns),
        datetime.now(),
        status
    )

    cursor.execute(insert_query, values)
    connection.commit()

    cursor.close()
    connection.close()

    print("Metadata logged to MySQL")
