import pandas as pd
import mysql.connector


def save_to_mysql(file_path, table_name):

    df = pd.read_csv(file_path)

    # 🔥 Fix datetime format
    if "publish_time" in df.columns:
        df["publish_time"] = pd.to_datetime(df["publish_time"], errors="coerce")
        df["publish_time"] = df["publish_time"].dt.strftime("%Y-%m-%d %H:%M:%S")

    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="youtube_pipeline"
    )

    cursor = connection.cursor()

    # 🔥 DROP TABLE ก่อนสร้างใหม่ (กัน schema mismatch)
    cursor.execute(f"DROP TABLE IF EXISTS {table_name}")

    # 🔥 สร้าง table ตาม column ของไฟล์
    column_definitions = []

    for col in df.columns:
        if "int" in str(df[col].dtype):
            column_definitions.append(f"{col} BIGINT")
        elif "float" in str(df[col].dtype):
            column_definitions.append(f"{col} DOUBLE")
        elif col == "publish_time":
            column_definitions.append(f"{col} DATETIME")
        else:
            column_definitions.append(f"{col} TEXT")

    create_table_query = f"""
        CREATE TABLE {table_name} (
            id INT AUTO_INCREMENT PRIMARY KEY,
            {", ".join(column_definitions)}
        )
    """

    cursor.execute(create_table_query)

    # 🔥 Insert Data
    columns = ", ".join(df.columns)
    placeholders = ", ".join(["%s"] * len(df.columns))

    insert_query = f"""
        INSERT INTO {table_name} ({columns})
        VALUES ({placeholders})
    """

    for _, row in df.iterrows():
        cursor.execute(insert_query, tuple(row))

    connection.commit()
    cursor.close()
    connection.close()

    print(f"Data saved to MySQL table: {table_name}")
