import pandas as pd

def cleanse_data(input_path, output_path):

    df = pd.read_csv(input_path)

    # Convert to numeric
    df["views"] = pd.to_numeric(df["views"], errors="coerce")
    df["likes"] = pd.to_numeric(df["likes"], errors="coerce")

    # Remove missing
    df = df.dropna()

    # Remove duplicates
    df = df.drop_duplicates()

    # Convert publish_time to datetime
    df["publish_time"] = pd.to_datetime(df["publish_time"], errors="coerce")

    # Create publish period
    def get_period(hour):
        if 5 <= hour < 12:
            return "Morning"
        elif 12 <= hour < 17:
            return "Afternoon"
        elif 17 <= hour < 21:
            return "Evening"
        else:
            return "Night"

    df["publish_period"] = df["publish_time"].dt.hour.apply(get_period)

    df.to_csv(output_path, index=False)

    print("Data Cleansing Complete")
