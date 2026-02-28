import pandas as pd
from datetime import datetime
from sklearn.preprocessing import MinMaxScaler


def prepare_data(input_path, output_path):

    print("Starting Data Preparation...")

    df = pd.read_csv(input_path)

    # ==========================
    # 1. Handle Missing Values
    # ==========================

    numeric_cols = ["views", "likes"]

    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")
        df[col] = df[col].fillna(df[col].median())

    # ==========================
    # 2. Convert publish_time properly
    # ==========================

    df["publish_time"] = pd.to_datetime(df["publish_time"], utc=True)

    # ใช้ utc now เพื่อให้ timezone ตรงกัน
    current_time = pd.Timestamp.utcnow()

    df["video_age_days"] = (current_time - df["publish_time"]).dt.days

    # ==========================
    # 3. Feature Engineering
    # ==========================

    df["engagement_rate"] = df["likes"] / df["views"]

    # ==========================
    # 4. Normalization
    # ==========================

    scaler = MinMaxScaler()

    df[["views", "likes", "video_age_days", "engagement_rate"]] = scaler.fit_transform(
        df[["views", "likes", "video_age_days", "engagement_rate"]]
    )

    # ==========================
    # Save Prepared Data
    # ==========================

    df.to_csv(output_path, index=False)

    print("Data Preparation Complete")
